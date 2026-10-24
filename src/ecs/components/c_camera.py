import pygame


class CCamera:
    """Ventana del mundo que se esta viendo.

    `rect` esta en coordenadas de mundo: x se mueve con el jugador a lo largo del
    planeta, y queda fijo porque el area de juego no hace scroll vertical.
    `player_screen_x` es la columna de pantalla donde se mantiene la nave.
    """

    def __init__(self, rect: pygame.Rect, player_screen_x: float) -> None:
        self.rect = rect
        self.player_screen_x = player_screen_x
