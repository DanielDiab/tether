class CLifetime:
    """Tiempo de vida en segundos; al agotarse la entidad se elimina."""

    def __init__(self, seconds: float) -> None:
        self.remaining = seconds
