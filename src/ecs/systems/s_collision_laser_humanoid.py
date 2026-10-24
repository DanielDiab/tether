import esper
import pygame

from src.create.prefab_creator import create_explosion
from src.ecs.components.c_game_state import CGameState
from src.ecs.components.c_humanoid_state import CHumanoidState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_laser import CTagLaser
from src.engine.collision import collide_world


def system_collision_laser_humanoid(world: esper.World, world_width: float,
                                    explosion_cfg: dict) -> None:
    """En Defender el laser tambien mata a los astronautas: disparar tiene costo."""
    for laser_entity, (l_t, l_s, _tag) in world.get_components(
            CTransform, CSurface, CTagLaser):
        for h_entity, (h_t, h_s, _h_st) in world.get_components(
                CTransform, CSurface, CHumanoidState):
            if not collide_world(l_t.pos, l_s.area, h_t.pos, h_s.area, world_width):
                continue
            center = pygame.Vector2(h_t.pos.x + h_s.area.w / 2.0,
                                    h_t.pos.y + h_s.area.h / 2.0)
            create_explosion(world, center, explosion_cfg)
            world.delete_entity(h_entity)
            world.delete_entity(laser_entity)
            states = world.get_component(CGameState)
            if states:
                states[0][1].humanoids_alive = max(0, states[0][1].humanoids_alive - 1)
            return
