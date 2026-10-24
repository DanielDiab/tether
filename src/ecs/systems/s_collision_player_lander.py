import esper
import pygame

from src.create.prefab_creator import create_explosion
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_game_state import CGameState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_lander import CTagLander
from src.engine.collision import collide_world
from src.engine.service_locator import ServiceLocator


def system_collision_player_lander(world: esper.World, player_entity: int,
                                   world_width: float, explosion_cfg: dict,
                                   player_cfg: dict, respawn_pos: pygame.Vector2) -> bool:
    """Choque jugador-Lander: cuesta una vida. Devuelve True si el jugador murio.

    Mientras parpadea (CBlink) el jugador es invulnerable; es el mismo truco de
    game feel del arcade para que no se pierdan dos vidas en el mismo instante.
    """
    if world.has_component(player_entity, CBlink):
        return False
    p_t = world.component_for_entity(player_entity, CTransform)
    p_s = world.component_for_entity(player_entity, CSurface)
    p_v = world.component_for_entity(player_entity, CVelocity)
    for _, (e_t, e_s, _tag) in world.get_components(CTransform, CSurface, CTagLander):
        if not collide_world(p_t.pos, p_s.area, e_t.pos, e_s.area, world_width):
            continue
        center = pygame.Vector2(p_t.pos.x + p_s.area.w / 2.0,
                                p_t.pos.y + p_s.area.h / 2.0)
        create_explosion(world, center, explosion_cfg)
        ServiceLocator.sounds_service.play(explosion_cfg["sound"])
        p_t.pos.xy = respawn_pos
        p_v.vel.xy = (0, 0)
        world.add_component(player_entity, CBlink(player_cfg["invulnerable_time"],
                                                  player_cfg["blink_interval"]))
        states = world.get_component(CGameState)
        if states:
            states[0][1].lives -= 1
        return True
    return False
