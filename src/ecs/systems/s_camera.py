import esper

from src.ecs.components.c_camera import CCamera
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.engine.world_math import wrap_x


def system_camera(world: esper.World, player_entity: int, world_width: float) -> None:
    """Mantiene la nave en una columna fija de la pantalla y mueve el mundo detras.

    Si no hay camara (bono sin implementar) el jugador simplemente se queda quieto en
    pantalla; aqui la camara es la que se desplaza por el cilindro del planeta.
    """
    c_t = world.component_for_entity(player_entity, CTransform)
    c_s = world.component_for_entity(player_entity, CSurface)
    player_center_x = c_t.pos.x + c_s.area.w / 2.0
    for _, c_cam in world.get_component(CCamera):
        c_cam.rect.x = int(wrap_x(player_center_x - c_cam.player_screen_x, world_width))
