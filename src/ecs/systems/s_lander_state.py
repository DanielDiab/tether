import random

import esper
import pygame

from src.ecs.components.c_game_state import CGameState
from src.ecs.components.c_humanoid_state import CHumanoidState, HumanoidState
from src.ecs.components.c_lander_state import CLanderState, LanderState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.engine.world_math import signed_delta_x


def system_lander_state(world: esper.World, delta_time: float, play_rect: pygame.Rect,
                        world_width: float) -> None:
    """Patron State del Lander, el enemigo que define a Defender.

    DESCEND baja al planeta, SEARCH busca astronautas, ABDUCT se los lleva al techo.
    """
    for entity, (c_t, c_v, c_s, c_lst) in world.get_components(
            CTransform, CVelocity, CSurface, CLanderState):
        if c_lst.state == LanderState.DESCEND:
            _do_descend(c_v, c_t, c_lst)
        elif c_lst.state == LanderState.SEARCH:
            _do_search(world, entity, c_t, c_v, c_s, c_lst, delta_time, world_width)
        elif c_lst.state == LanderState.ABDUCT:
            _do_abduct(world, c_t, c_v, c_lst, play_rect)


def _do_descend(c_v: CVelocity, c_t: CTransform, c_lst: CLanderState) -> None:
    c_v.vel.xy = (0, c_lst.velocity_descend)
    if c_t.pos.y >= c_lst.descend_until_y:
        c_lst.state = LanderState.SEARCH


def _nearest_free_humanoid(world: esper.World, c_t: CTransform,
                           world_width: float) -> tuple[int | None, float]:
    """Astronauta libre mas cercano midiendo la distancia por el cilindro del mundo."""
    best_entity: int | None = None
    best_distance = float("inf")
    for entity, (h_t, h_st) in world.get_components(CTransform, CHumanoidState):
        if h_st.state != HumanoidState.WALK or h_st.captor is not None:
            continue
        distance = abs(signed_delta_x(c_t.pos.x, h_t.pos.x, world_width))
        if distance < best_distance:
            best_distance = distance
            best_entity = entity
    return best_entity, best_distance


def _do_search(world: esper.World, entity: int, c_t: CTransform, c_v: CVelocity,
               c_s: CSurface, c_lst: CLanderState, delta_time: float,
               world_width: float) -> None:
    target, distance_x = _nearest_free_humanoid(world, c_t, world_width)
    if target is None:
        # Sin astronautas libres patrulla cambiando de rumbo cada cierto tiempo
        c_lst.search_timer -= delta_time
        if c_lst.search_timer <= 0:
            c_lst.search_timer = c_lst.search_interval
            c_v.vel.xy = (random.choice((-1, 1)) * c_lst.velocity_search,
                          random.uniform(-0.3, 0.3) * c_lst.velocity_search)
        return

    h_t = world.component_for_entity(target, CTransform)
    h_s = world.component_for_entity(target, CSurface)
    delta_x = signed_delta_x(c_t.pos.x, h_t.pos.x, world_width)
    delta_y = h_t.pos.y - h_s.area.h - c_t.pos.y
    direction = pygame.Vector2(delta_x, delta_y)
    if direction.length_squared() > 0:
        c_v.vel = direction.normalize() * c_lst.velocity_search

    if distance_x <= c_lst.abduct_range and abs(delta_y) <= c_lst.abduct_range:
        # Captura: el astronauta pasa a ABDUCTED y queda colgando del Lander
        c_h_st = world.component_for_entity(target, CHumanoidState)
        c_h_st.state = HumanoidState.ABDUCTED
        c_h_st.captor = entity
        c_lst.target = target
        c_lst.state = LanderState.ABDUCT
        c_t.pos.x = h_t.pos.x + (h_s.area.w - c_s.area.w) / 2.0


def _do_abduct(world: esper.World, c_t: CTransform, c_v: CVelocity, c_lst: CLanderState,
               play_rect: pygame.Rect) -> None:
    c_v.vel.xy = (0, -c_lst.velocity_abduct)
    target = c_lst.target
    if target is None or not world.entity_exists(target):
        c_lst.target = None
        c_lst.state = LanderState.SEARCH
        return
    if c_t.pos.y > play_rect.y:
        return
    # Llego al techo con el astronauta: se pierde el astronauta.
    # TODO semana 3: aqui el Lander debe convertirse en Mutant en lugar de soltarlo.
    world.delete_entity(target)
    states = world.get_component(CGameState)
    if states:
        states[0][1].humanoids_alive = max(0, states[0][1].humanoids_alive - 1)
    c_lst.target = None
    c_lst.state = LanderState.SEARCH
    c_t.pos.y = play_rect.y
