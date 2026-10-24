from enum import Enum


class HumanoidState(Enum):
    WALK = 0        # camina por la superficie del planeta
    ABDUCTED = 1    # un Lander lo esta subiendo
    FALLING = 2     # su captor fue destruido y esta cayendo
    CARRIED = 3     # la nave del jugador lo lleva
    DEAD = 4


class CHumanoidState:
    """Estado del astronauta. `captor` es la entidad que lo sujeta (Lander o jugador)."""

    def __init__(self, walk_velocity: float) -> None:
        self.state = HumanoidState.WALK
        self.walk_velocity = walk_velocity
        self.direction = 1
        self.captor: int | None = None
