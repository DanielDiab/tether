import esper
import pygame

from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_camera import CCamera
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.engine.world_math import world_to_screen_x


def system_rendering(world: esper.World, screen: pygame.Surface, c_cam: CCamera,
                     world_width: float, play_rect: pygame.Rect) -> None:
    """Dibuja los sprites convirtiendo coordenadas de mundo a coordenadas de pantalla.

    El recorte al area de juego evita que una nave se dibuje encima del radar o del HUD.
    """
    screen.set_clip(play_rect)
    for entity, (c_t, c_s) in world.get_components(CTransform, CSurface):
        if world.has_component(entity, CBlink):
            if not world.component_for_entity(entity, CBlink).visible:
                continue
        screen_x = world_to_screen_x(c_t.pos.x, c_cam.rect.x, world_width,
                                     play_rect.width, c_s.area.w)
        if screen_x is None:
            continue
        surface = c_s.surf
        area = c_s.area
        if c_s.flip_h:
            surface = pygame.transform.flip(surface.subsurface(area), True, False)
            area = surface.get_rect()
        screen.blit(surface, (play_rect.x + screen_x, c_t.pos.y), area=area)
    screen.set_clip(None)
