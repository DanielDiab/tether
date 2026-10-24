"""Colision AABB en un mundo cilindrico.

No se puede usar `Rect.colliderect` directamente: dos entidades pueden estar a 3 pixeles
una de otra y tener coordenadas x en extremos opuestos del mundo (una en x=5 y la otra
en x=1917). La prueba se hace sobre la distancia mas corta alrededor del cilindro.
"""
import pygame

from src.engine.world_math import signed_delta_x


def collide_world(pos_a: pygame.Vector2, size_a: pygame.Rect,
                  pos_b: pygame.Vector2, size_b: pygame.Rect,
                  world_width: float) -> bool:
    center_a_x = pos_a.x + size_a.w / 2.0
    center_b_x = pos_b.x + size_b.w / 2.0
    delta_x = abs(signed_delta_x(center_a_x, center_b_x, world_width))
    if delta_x * 2 >= size_a.w + size_b.w:
        return False
    center_a_y = pos_a.y + size_a.h / 2.0
    center_b_y = pos_b.y + size_b.h / 2.0
    return abs(center_b_y - center_a_y) * 2 < size_a.h + size_b.h
