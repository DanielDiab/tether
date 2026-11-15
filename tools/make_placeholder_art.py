#!/usr/bin/python3
"""Genera los sprites PLACEHOLDER del juego.

Sirve para trabajar mientras no hay arte definitivo. Las dimensiones son las
que espera assets/cfg/*.json, asi que al reemplazar un PNG por el final basta con
respetar el tamaño de cuadro indicado abajo y no hay que tocar codigo.

Uso: python tools/make_placeholder_art.py
"""
import os
import random

import pygame

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "assets", "img")

WHITE = (255, 255, 255)
YELLOW = (255, 230, 60)
CYAN = (90, 230, 255)
GREEN = (70, 230, 90)
RED = (255, 90, 70)
ORANGE = (255, 160, 40)


def sheet(frame_w: int, frame_h: int, frames: int) -> pygame.Surface:
    surface = pygame.Surface((frame_w * frames, frame_h), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))
    return surface


def save(surface: pygame.Surface, name: str) -> None:
    pygame.image.save(surface, os.path.join(OUT, name))
    print(f"  {name}: {surface.get_width()}x{surface.get_height()}")


def make_player() -> None:
    """Nave: 2 cuadros de 16x8 (IDLE y THRUST). Mira a la DERECHA; el motor la voltea."""
    surface = sheet(16, 8, 2)
    for frame in range(2):
        x = frame * 16
        # Casco: cuña apuntando a la derecha
        pygame.draw.polygon(surface, WHITE, [(x + 15, 4), (x + 5, 1), (x + 5, 6)])
        pygame.draw.rect(surface, CYAN, (x + 2, 3, 4, 2))
        if frame == 1:
            # Llama del propulsor
            pygame.draw.polygon(surface, ORANGE, [(x + 2, 3), (x + 2, 5), (x, 4)])
    save(surface, "player.png")


def make_lander() -> None:
    """Lander: 2 cuadros de 12x12."""
    surface = sheet(12, 12, 2)
    for frame in range(2):
        x = frame * 12
        pygame.draw.rect(surface, GREEN, (x + 3, 1, 6, 4))
        pygame.draw.rect(surface, WHITE, (x + 5, 2, 2, 2))
        pygame.draw.line(surface, GREEN, (x + 3, 5), (x + 1, 10))
        pygame.draw.line(surface, GREEN, (x + 8, 5), (x + 10, 10))
        pygame.draw.line(surface, GREEN, (x + 5, 5), (x + 5 + frame, 10))
        pygame.draw.line(surface, GREEN, (x + 7, 5), (x + 7 - frame, 10))
    save(surface, "lander.png")


def make_humanoid() -> None:
    """Astronauta: 2 cuadros de 6x8 (animacion de caminar)."""
    surface = sheet(6, 8, 2)
    for frame in range(2):
        x = frame * 6
        pygame.draw.rect(surface, CYAN, (x + 2, 0, 2, 2))
        pygame.draw.rect(surface, CYAN, (x + 2, 2, 2, 3))
        if frame == 0:
            pygame.draw.line(surface, CYAN, (x + 2, 5), (x + 1, 7))
            pygame.draw.line(surface, CYAN, (x + 3, 5), (x + 4, 7))
        else:
            pygame.draw.line(surface, CYAN, (x + 2, 5), (x + 2, 7))
            pygame.draw.line(surface, CYAN, (x + 3, 5), (x + 3, 7))
    save(surface, "humanoid.png")


def make_laser() -> None:
    """Laser: un unico cuadro de 24x2."""
    surface = sheet(24, 2, 1)
    pygame.draw.rect(surface, YELLOW, (0, 0, 24, 1))
    pygame.draw.rect(surface, WHITE, (16, 0, 8, 2))
    save(surface, "laser.png")


def make_explosion() -> None:
    """Explosion: 6 cuadros de 16x16, particulas que se expanden."""
    surface = sheet(16, 16, 6)
    rng = random.Random(1981)
    particles = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(14)]
    for frame in range(6):
        ox = frame * 16
        radius = 1.0 + frame * 1.3
        color = (WHITE, YELLOW, ORANGE, RED)[min(3, frame // 2)]
        for dx, dy in particles:
            px = ox + 8 + dx * radius
            py = 8 + dy * radius
            if 0 <= px - ox < 16 and 0 <= py < 16:
                surface.set_at((int(px), int(py)), color)
    save(surface, "explosion.png")


if __name__ == "__main__":
    pygame.init()
    os.makedirs(OUT, exist_ok=True)
    print("Generando sprites placeholder en assets/img/")
    make_player()
    make_lander()
    make_humanoid()
    make_laser()
    make_explosion()
    pygame.quit()
