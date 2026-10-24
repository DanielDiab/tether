import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface


def system_animation(world: esper.World, delta_time: float) -> None:
    for _, (c_s, c_a) in world.get_components(CSurface, CAnimation):
        anim = c_a.animations[c_a.curr_anim]
        c_a.curr_anim_time -= delta_time
        # Un while por si un frame lento debe avanzar mas de un cuadro
        while c_a.curr_anim_time <= 0:
            c_a.curr_anim_time += anim.framerate_time
            c_a.curr_frame += 1
            if c_a.curr_frame > anim.end:
                c_a.curr_frame = anim.start
                c_a.finished = True
        c_s.area.x = c_s.area.w * c_a.curr_frame


def set_animation(c_a: CAnimation, name: str) -> None:
    """Cambia la animacion actual; no hace nada si ya es la que se esta reproduciendo."""
    if c_a.curr_anim == name:
        return
    anim = c_a.animations[name]
    c_a.curr_anim = name
    c_a.curr_frame = anim.start
    c_a.curr_anim_time = anim.framerate_time
    c_a.finished = False
