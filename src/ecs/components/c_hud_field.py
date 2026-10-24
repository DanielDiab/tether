class CHudField:
    """Enlaza un CText con un campo de CGameState para que el HUD se actualice solo."""

    def __init__(self, field: str, fmt: str = "{}") -> None:
        self.field = field
        self.fmt = fmt
