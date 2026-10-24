import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_terrain import CTerrain
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_player_limits(world: esper.World, play_rect: pygame.Rect) -> None:
    """La nave no sale del area de juego ni atraviesa el terreno.

    El limite inferior no es una linea recta: es la altura del terreno justo debajo
    de la nave, asi que la nave "roza" las montañas igual que en el original.
    """
    terrains = world.get_component(CTerrain)
    c_terrain = terrains[0][1] if terrains else None
    for _, (c_t, c_v, c_s, _tag) in world.get_components(
            CTransform, CVelocity, CSurface, CTagPlayer):
        if c_t.pos.y < play_rect.y:
            c_t.pos.y = play_rect.y
            c_v.vel.y = max(0.0, c_v.vel.y)
        floor_y = play_rect.bottom
        if c_terrain is not None:
            floor_y = c_terrain.height_at(c_t.pos.x + c_s.area.w / 2.0)
        if c_t.pos.y + c_s.area.h > floor_y:
            c_t.pos.y = floor_y - c_s.area.h
            c_v.vel.y = min(0.0, c_v.vel.y)
