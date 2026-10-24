import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_player_state import CPlayerState, Facing, PlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_animation import set_animation


def system_player_state(world: esper.World) -> None:
    """Patron State: la animacion y el volteo del sprite se derivan del estado."""
    for _, (c_v, c_s, c_a, c_pst) in world.get_components(
            CVelocity, CSurface, CAnimation, CPlayerState):
        if c_v.vel.x < 0:
            c_pst.facing = Facing.LEFT
        elif c_v.vel.x > 0:
            c_pst.facing = Facing.RIGHT
        c_s.flip_h = c_pst.facing == Facing.LEFT

        if c_pst.state == PlayerState.IDLE:
            set_animation(c_a, "IDLE")
            if c_v.vel.length_squared() > 0:
                c_pst.state = PlayerState.THRUST
        elif c_pst.state == PlayerState.THRUST:
            set_animation(c_a, "THRUST")
            if c_v.vel.length_squared() == 0:
                c_pst.state = PlayerState.IDLE
