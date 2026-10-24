from enum import Enum


class LanderState(Enum):
    DESCEND = 0   # baja desde la parte alta del area de juego
    SEARCH = 1    # patrulla buscando un astronauta
    ABDUCT = 2    # sube con un astronauta hacia el techo
    ATTACK = 3    # persigue al jugador (se usa al convertirse en Mutant)


class CLanderState:
    """Patron State del Lander, el enemigo basico de Defender.

    Los parametros vienen de enemies.json para poder ajustar la dificultad sin
    recompilar nada.
    """

    def __init__(self, cfg: dict) -> None:
        self.state = LanderState.DESCEND
        self.velocity_descend = cfg["velocity_descend"]
        self.velocity_search = cfg["velocity_search"]
        self.velocity_abduct = cfg["velocity_abduct"]
        self.descend_until_y = 0.0
        self.search_timer = 0.0
        self.search_interval = cfg["search_interval"]
        self.abduct_range = cfg["abduct_range"]
        self.target: int | None = None
