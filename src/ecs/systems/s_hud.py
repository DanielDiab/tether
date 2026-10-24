import esper

from src.ecs.components.c_game_state import CGameState
from src.ecs.components.c_hud_field import CHudField
from src.ecs.components.c_text import CText


def system_hud(world: esper.World) -> None:
    """Copia los valores del estado de partida a los textos del HUD."""
    states = world.get_component(CGameState)
    if not states:
        return
    c_state = states[0][1]
    for _, (c_text, c_field) in world.get_components(CText, CHudField):
        c_text.text = c_field.fmt.format(getattr(c_state, c_field.field))
