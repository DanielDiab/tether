class CBlink:
    """Game feel: parpadeo temporal de una entidad (invulnerabilidad del jugador)."""

    def __init__(self, duration: float, interval: float) -> None:
        self.remaining = duration
        self.interval = interval
        self.timer = interval
        self.visible = True
