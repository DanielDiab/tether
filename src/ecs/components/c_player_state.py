from enum import Enum


class PlayerState(Enum):
    IDLE = 0
    THRUST = 1


class Facing(Enum):
    LEFT = -1
    RIGHT = 1


class CPlayerState:
    """Patron State del jugador. La direccion a la que mira decide el volteo del
    sprite y hacia donde sale el laser, igual que en el Defender original."""

    def __init__(self) -> None:
        self.state = PlayerState.IDLE
        self.facing = Facing.RIGHT
