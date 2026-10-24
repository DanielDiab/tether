import esper

from src.ecs.components.c_humanoid_state import CHumanoidState, HumanoidState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.collision import collide_world


def system_collision_player_humanoid(world: esper.World, world_width: float) -> None:
    """La nave recoge al astronauta que cae; solo puede llevar uno a la vez."""
    players = world.get_components(CTransform, CSurface, CTagPlayer)
    if not players:
        return
    player_entity, (p_t, p_s, _tag) = players[0]
    already_carrying = any(
        c_hst.state == HumanoidState.CARRIED and c_hst.captor == player_entity
        for _, c_hst in world.get_component(CHumanoidState))
    if already_carrying:
        return
    for _, (h_t, h_s, c_hst) in world.get_components(CTransform, CSurface, CHumanoidState):
        if c_hst.state != HumanoidState.FALLING:
            continue
        if collide_world(p_t.pos, p_s.area, h_t.pos, h_s.area, world_width):
            c_hst.state = HumanoidState.CARRIED
            c_hst.captor = player_entity
            return
