"""Servicio de fuentes.

Si la fuente pedida no existe usa la fuente por defecto de pygame, para que el HUD
siga dibujandose mientras no esten los .ttf definitivos del juego.
"""
import os

import pygame


class FontService:
    def __init__(self) -> None:
        self._fonts: dict[tuple[str, int], pygame.font.Font] = {}

    def get(self, path: str, size: int) -> pygame.font.Font:
        key = (path, size)
        if key not in self._fonts:
            if path and os.path.isfile(path):
                self._fonts[key] = pygame.font.Font(path, size)
            else:
                self._fonts[key] = pygame.font.Font(None, size)
        return self._fonts[key]
