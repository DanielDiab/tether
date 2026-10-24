class CGameState:
    """Estado global de la partida, en una unica entidad "singleton".

    Mantenerlo como componente (y no como atributo de la escena) permite que los
    sistemas de puntaje, HUD y colisiones lo lean y escriban como cualquier otro dato
    del mundo ECS.
    """

    def __init__(self, lives: int, smart_bombs: int) -> None:
        self.score = 0
        self.lives = lives
        self.smart_bombs = smart_bombs
        self.wave = 1
        self.humanoids_alive = 0
        self.paused = False
