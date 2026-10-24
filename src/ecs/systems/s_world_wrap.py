import esper

from src.ecs.components.c_transform import CTransform
from src.engine.world_math import wrap_x


def system_world_wrap(world: esper.World, world_width: float) -> None:
    """Normaliza la x de todas las entidades al rango del mundo.

    Gracias a esto el planeta es un cilindro: salir por un extremo equivale a entrar
    por el otro, sin ningun caso especial en el resto de los sistemas.
    """
    for _, c_t in world.get_component(CTransform):
        c_t.pos.x = wrap_x(c_t.pos.x, world_width)
