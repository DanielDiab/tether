import esper
import pygame

from src.ecs.components.c_camera import CCamera
from src.ecs.components.c_terrain import CTerrain


def system_rendering_terrain(world: esper.World, screen: pygame.Surface, c_cam: CCamera,
                             play_rect: pygame.Rect, color: pygame.Color) -> None:
    """Dibuja el perfil montañoso del planeta.

    Cada segmento se intenta dibujar en tres posiciones (una vuelta atras, la actual y
    una vuelta adelante) para que la costura del cilindro no se note nunca.
    """
    screen.set_clip(play_rect)
    for _, c_terrain in world.get_component(CTerrain):
        width = c_terrain.world_width
        points = c_terrain.points
        for offset in (-width, 0, width):
            for i in range(len(points) - 1):
                x0, y0 = points[i]
                x1, y1 = points[i + 1]
                sx0 = x0 - c_cam.rect.x + offset
                sx1 = x1 - c_cam.rect.x + offset
                if sx1 < 0 or sx0 > play_rect.width:
                    continue
                pygame.draw.line(screen, color,
                                 (play_rect.x + sx0, y0),
                                 (play_rect.x + sx1, y1))
    screen.set_clip(None)
