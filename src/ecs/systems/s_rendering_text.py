import esper
import pygame

from src.ecs.components.c_text import CText
from src.engine.service_locator import ServiceLocator


def system_rendering_text(world: esper.World, screen: pygame.Surface) -> None:
    """Dibuja los textos de menus y HUD pidiendo las fuentes al Service Locator."""
    for _, c_text in world.get_component(CText):
        font = ServiceLocator.fonts_service.get(c_text.font_path, c_text.size)
        surface = font.render(c_text.text, False, c_text.color)
        rect = surface.get_rect()
        if c_text.align == "center":
            rect.midtop = (int(c_text.pos.x), int(c_text.pos.y))
        elif c_text.align == "right":
            rect.topright = (int(c_text.pos.x), int(c_text.pos.y))
        else:
            rect.topleft = (int(c_text.pos.x), int(c_text.pos.y))
        screen.blit(surface, rect)
