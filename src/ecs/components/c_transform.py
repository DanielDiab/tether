import pygame


class CTransform:
    """Posicion de la entidad en coordenadas de MUNDO (no de pantalla).

    El mundo de Defender es mucho mas ancho que la pantalla; la conversion a pantalla
    la hace el sistema de render usando la camara.
    """

    def __init__(self, pos: pygame.Vector2) -> None:
        self.pos = pygame.Vector2(pos)
