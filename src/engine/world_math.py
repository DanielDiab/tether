"""Matematicas del mundo de Defender.

El planeta es un cilindro: el mundo mide `world_width` pixeles y su borde derecho se
pega con el izquierdo. Por eso ninguna distancia horizontal se puede calcular con una
resta simple, hay que tomar siempre el camino mas corto alrededor del cilindro.
"""


def wrap_x(x: float, world_width: float) -> float:
    """Lleva una x de mundo al rango [0, world_width)."""
    return x % world_width


def signed_delta_x(from_x: float, to_x: float, world_width: float) -> float:
    """Distancia horizontal con signo por el camino mas corto del cilindro.

    El resultado esta en [-world_width/2, world_width/2): positivo si `to_x` queda a
    la derecha. Es lo que usan la camara y las IAs para decidir hacia donde ir.
    """
    half = world_width / 2.0
    return (to_x - from_x + half) % world_width - half


def distance_x(from_x: float, to_x: float, world_width: float) -> float:
    return abs(signed_delta_x(from_x, to_x, world_width))


def world_to_screen_x(world_x: float, camera_left: float, world_width: float,
                      screen_width: float, sprite_width: float = 0.0) -> float | None:
    """Convierte una x de mundo a x de pantalla, o None si no es visible.

    Se prueba tambien la copia "dando la vuelta" al cilindro, de modo que una entidad
    que esta cerca del borde del mundo aparece correctamente aunque la camara este al
    otro lado de la costura.
    """
    dx = (world_x - camera_left) % world_width
    if dx > world_width - sprite_width:
        dx -= world_width
    if -sprite_width < dx < screen_width:
        return dx
    return None
