import random

import esper
import pygame

from src.ecs.components.c_game_state import CGameState
from src.ecs.components.c_humanoid_state import CHumanoidState, HumanoidState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_terrain import CTerrain
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def system_humanoid(world: esper.World, delta_time: float, play_rect: pygame.Rect,
                    humanoid_cfg: dict) -> None:
    """Patron State de los astronautas.

    WALK caminan por la superficie, ABDUCTED cuelgan del Lander que los capturo,
    FALLING caen cuando su captor muere y CARRIED viajan con la nave del jugador
    hasta que esta los deja de nuevo en el suelo.
    """
    terrains = world.get_component(CTerrain)
    c_terrain = terrains[0][1] if terrains else None
    states = world.get_component(CGameState)
    c_state = states[0][1] if states else None

    for entity, (c_t, c_v, c_s, c_hst) in world.get_components(
            CTransform, CVelocity, CSurface, CHumanoidState):
        if c_hst.state == HumanoidState.WALK:
            _do_walk(c_t, c_v, c_s, c_hst, c_terrain, delta_time, humanoid_cfg)
        elif c_hst.state == HumanoidState.ABDUCTED:
            _do_abducted(world, c_t, c_v, c_s, c_hst)
        elif c_hst.state == HumanoidState.FALLING:
            _do_falling(c_t, c_v, c_s, c_hst, c_terrain, humanoid_cfg)
        elif c_hst.state == HumanoidState.CARRIED:
            _do_carried(world, c_t, c_v, c_s, c_hst, c_terrain, humanoid_cfg, c_state)

        if c_hst.state != HumanoidState.ABDUCTED:
            c_t.pos.y = min(c_t.pos.y, play_rect.bottom - c_s.area.h)


def _ground_y(c_terrain: CTerrain | None, c_t: CTransform, c_s: CSurface,
              play_rect_bottom: float = 0.0) -> float:
    if c_terrain is None:
        return play_rect_bottom
    return c_terrain.height_at(c_t.pos.x + c_s.area.w / 2.0) - c_s.area.h


def _do_walk(c_t: CTransform, c_v: CVelocity, c_s: CSurface, c_hst: CHumanoidState,
             c_terrain: CTerrain | None, delta_time: float, humanoid_cfg: dict) -> None:
    c_v.vel.xy = (c_hst.direction * c_hst.walk_velocity, 0)
    c_t.pos.y = _ground_y(c_terrain, c_t, c_s, c_t.pos.y)
    # De vez en cuando cambia de sentido, para que la superficie no se vea estatica
    if random.random() < humanoid_cfg["turn_chance_per_second"] * delta_time:
        c_hst.direction *= -1


def _do_abducted(world: esper.World, c_t: CTransform, c_v: CVelocity, c_s: CSurface,
                 c_hst: CHumanoidState) -> None:
    c_v.vel.xy = (0, 0)
    captor = c_hst.captor
    if captor is None or not world.entity_exists(captor):
        c_hst.state = HumanoidState.FALLING
        c_hst.captor = None
        return
    cap_t = world.component_for_entity(captor, CTransform)
    cap_s = world.component_for_entity(captor, CSurface)
    c_t.pos.x = cap_t.pos.x + (cap_s.area.w - c_s.area.w) / 2.0
    c_t.pos.y = cap_t.pos.y + cap_s.area.h


def _do_falling(c_t: CTransform, c_v: CVelocity, c_s: CSurface, c_hst: CHumanoidState,
                c_terrain: CTerrain | None, humanoid_cfg: dict) -> None:
    c_v.vel.xy = (0, humanoid_cfg["fall_velocity"])
    ground_y = _ground_y(c_terrain, c_t, c_s, c_t.pos.y)
    if c_t.pos.y >= ground_y:
        # Aterriza sano y salvo y vuelve a caminar
        c_t.pos.y = ground_y
        c_hst.state = HumanoidState.WALK


def _do_carried(world: esper.World, c_t: CTransform, c_v: CVelocity, c_s: CSurface,
                c_hst: CHumanoidState, c_terrain: CTerrain | None, humanoid_cfg: dict,
                c_state: CGameState | None) -> None:
    c_v.vel.xy = (0, 0)
    captor = c_hst.captor
    if captor is None or not world.entity_exists(captor):
        c_hst.state = HumanoidState.FALLING
        c_hst.captor = None
        return
    cap_t = world.component_for_entity(captor, CTransform)
    cap_s = world.component_for_entity(captor, CSurface)
    c_t.pos.x = cap_t.pos.x + (cap_s.area.w - c_s.area.w) / 2.0
    c_t.pos.y = cap_t.pos.y + cap_s.area.h
    # Si la nave vuela pegada al suelo, el astronauta se baja y se anota el rescate
    ground_y = _ground_y(c_terrain, c_t, c_s, c_t.pos.y)
    if c_t.pos.y >= ground_y - humanoid_cfg["drop_distance"]:
        c_t.pos.y = ground_y
        c_hst.state = HumanoidState.WALK
        c_hst.captor = None
        if c_state is not None:
            c_state.score += humanoid_cfg["score_rescue"]
