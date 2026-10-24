import esper
import pygame

from src.create.prefab_creator import create_explosion
from src.ecs.components.c_game_state import CGameState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_lander import CTagLander
from src.ecs.components.tags.c_tag_laser import CTagLaser
from src.engine.collision import collide_world
from src.engine.service_locator import ServiceLocator


def system_collision_laser_lander(world: esper.World, world_width: float,
                                  explosion_cfg: dict, score_cfg: dict) -> None:
    lasers = world.get_components(CTransform, CSurface, CTagLaser)
    landers = world.get_components(CTransform, CSurface, CTagLander)
    states = world.get_component(CGameState)
    for laser_entity, (l_t, l_s, _l_tag) in lasers:
        for lander_entity, (e_t, e_s, _e_tag) in landers:
            if not collide_world(l_t.pos, l_s.area, e_t.pos, e_s.area, world_width):
                continue
            center = pygame.Vector2(e_t.pos.x + e_s.area.w / 2.0,
                                    e_t.pos.y + e_s.area.h / 2.0)
            create_explosion(world, center, explosion_cfg)
            ServiceLocator.sounds_service.play(explosion_cfg["sound"])
            world.delete_entity(lander_entity)
            world.delete_entity(laser_entity)
            if states:
                states[0][1].score += score_cfg["lander"]
            break
