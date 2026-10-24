import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.tags.c_tag_explosion import CTagExplosion


def system_explosion_kill(world: esper.World) -> None:
    for entity, (c_a, _tag) in world.get_components(CAnimation, CTagExplosion):
        if c_a.finished:
            world.delete_entity(entity)
