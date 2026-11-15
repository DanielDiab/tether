"""Fabrica de entidades.

Es el unico lugar que sabe que componentes forman cada tipo de entidad del juego, y
toma todos los numeros de los archivos de configuracion. Las texturas se piden al
Service Locator, nunca se cargan aqui.
"""
import random

import esper
import pygame

from src.ecs.components.c_animation import AnimationData, CAnimation
from src.ecs.components.c_camera import CCamera
from src.ecs.components.c_game_state import CGameState
from src.ecs.components.c_humanoid_state import CHumanoidState
from src.ecs.components.c_hud_field import CHudField
from src.ecs.components.c_input_command import CInputCommand, InputDevice
from src.ecs.components.c_lander_state import CLanderState
from src.ecs.components.c_lifetime import CLifetime
from src.ecs.components.c_player_state import CPlayerState, Facing
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_terrain import CTerrain
from src.ecs.components.c_text import CText
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_humanoid import CTagHumanoid
from src.ecs.components.tags.c_tag_lander import CTagLander
from src.ecs.components.tags.c_tag_laser import CTagLaser
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator


def _vec(cfg: dict) -> pygame.Vector2:
    return pygame.Vector2(cfg["x"], cfg["y"])


def _color(cfg) -> pygame.Color:
    if isinstance(cfg, dict):
        return pygame.Color(cfg["r"], cfg["g"], cfg["b"])
    return pygame.Color(*cfg)


def create_sprite(world: esper.World, pos: pygame.Vector2, vel: pygame.Vector2,
                  texture: pygame.Surface) -> int:
    entity = world.create_entity()
    world.add_component(entity, CTransform(pos))
    world.add_component(entity, CVelocity(vel))
    world.add_component(entity, CSurface(texture))
    return entity


def _add_animation(world: esper.World, entity: int, animations_cfg: dict,
                   initial_anim: str) -> None:
    number_frames = animations_cfg["number_frames"]
    animations = [AnimationData(a["name"], a["start"], a["end"], a["framerate"],
                                number_frames)
                  for a in animations_cfg["list"]]
    c_a = CAnimation(number_frames, animations, initial_anim)
    world.add_component(entity, c_a)
    # Con animacion el area pasa a ser un solo cuadro del spritesheet
    c_s = world.component_for_entity(entity, CSurface)
    c_s.area.w = c_s.surf.get_width() // number_frames
    c_s.area.x = c_s.area.w * c_a.curr_frame


def _add_optional_animation(world: esper.World, entity: int, cfg: dict) -> None:
    if "animations" in cfg:
        _add_animation(world, entity, cfg["animations"],
                       cfg["animations"]["list"][0]["name"])


# ------------------------------------------------------------------ entidades del juego
def create_player(world: esper.World, player_cfg: dict, pos: pygame.Vector2) -> int:
    texture = ServiceLocator.textures_service.get(player_cfg["image"])
    entity = create_sprite(world, pygame.Vector2(pos), pygame.Vector2(0, 0), texture)
    _add_animation(world, entity, player_cfg["animations"], "IDLE")
    world.add_component(entity, CPlayerState())
    world.add_component(entity, CTagPlayer())
    return entity


def create_laser(world: esper.World, player_pos: pygame.Vector2, player_area: pygame.Rect,
                 facing: Facing, laser_cfg: dict) -> int:
    """El laser es un haz horizontal que sale en la direccion de la nave."""
    texture = ServiceLocator.textures_service.get(laser_cfg["image"])
    vel = pygame.Vector2(facing.value * laser_cfg["velocity"], 0)
    entity = create_sprite(world, pygame.Vector2(0, 0), vel, texture)
    _add_optional_animation(world, entity, laser_cfg)
    c_t = world.component_for_entity(entity, CTransform)
    c_s = world.component_for_entity(entity, CSurface)
    nose_x = player_pos.x + (player_area.w if facing == Facing.RIGHT else -c_s.area.w)
    c_t.pos.xy = (nose_x, player_pos.y + (player_area.h - c_s.area.h) / 2.0)
    world.add_component(entity, CLifetime(laser_cfg["lifetime"]))
    world.add_component(entity, CTagLaser())
    ServiceLocator.sounds_service.play(laser_cfg["sound"])
    return entity


def create_lander(world: esper.World, pos: pygame.Vector2, lander_cfg: dict,
                  descend_until_y: float) -> int:
    texture = ServiceLocator.textures_service.get(lander_cfg["image"])
    entity = create_sprite(world, pygame.Vector2(pos), pygame.Vector2(0, 0), texture)
    _add_optional_animation(world, entity, lander_cfg)
    c_lst = CLanderState(lander_cfg)
    c_lst.descend_until_y = descend_until_y
    world.add_component(entity, c_lst)
    world.add_component(entity, CTagLander())
    return entity


def create_humanoid(world: esper.World, pos: pygame.Vector2, humanoid_cfg: dict) -> int:
    texture = ServiceLocator.textures_service.get(humanoid_cfg["image"])
    entity = create_sprite(world, pygame.Vector2(pos), pygame.Vector2(0, 0), texture)
    _add_optional_animation(world, entity, humanoid_cfg)
    c_hst = CHumanoidState(humanoid_cfg["walk_velocity"])
    c_hst.direction = random.choice((-1, 1))
    world.add_component(entity, c_hst)
    world.add_component(entity, CTagHumanoid())
    return entity


def create_explosion(world: esper.World, center: pygame.Vector2,
                     explosion_cfg: dict) -> int:
    texture = ServiceLocator.textures_service.get(explosion_cfg["image"])
    entity = create_sprite(world, pygame.Vector2(0, 0), pygame.Vector2(0, 0), texture)
    _add_animation(world, entity, explosion_cfg["animations"], "EXPLODE")
    c_t = world.component_for_entity(entity, CTransform)
    c_s = world.component_for_entity(entity, CSurface)
    c_t.pos.xy = center - pygame.Vector2(c_s.area.size) / 2.0
    world.add_component(entity, CTagExplosion())
    return entity


# -------------------------------------------------------------- entidades de "escenario"
def create_terrain(world: esper.World, terrain_cfg: dict, play_rect: pygame.Rect,
                   world_width: float) -> int:
    """Genera el perfil montañoso del planeta de forma procedural.

    El ultimo vertice repite la altura del primero para que la union del cilindro sea
    invisible. La semilla esta en el JSON, asi el mismo nivel siempre sale igual.
    """
    rng = random.Random(terrain_cfg["seed"])
    segments = terrain_cfg["segments"]
    step = world_width / segments
    min_y = play_rect.bottom - terrain_cfg["max_height"]
    max_y = play_rect.bottom - terrain_cfg["min_height"]
    points: list[tuple[float, float]] = []
    first_y = rng.uniform(min_y, max_y)
    for i in range(segments):
        y = first_y if i == 0 else rng.uniform(min_y, max_y)
        points.append((i * step, y))
    points.append((world_width, first_y))
    entity = world.create_entity()
    world.add_component(entity, CTerrain(points, world_width))
    return entity


def create_camera(world: esper.World, play_rect: pygame.Rect,
                  player_screen_x: float) -> int:
    entity = world.create_entity()
    rect = pygame.Rect(0, play_rect.y, play_rect.width, play_rect.height)
    world.add_component(entity, CCamera(rect, player_screen_x))
    return entity


def create_game_state(world: esper.World, game_cfg: dict) -> int:
    entity = world.create_entity()
    world.add_component(entity, CGameState(game_cfg["lives"], game_cfg["smart_bombs"]))
    return entity


def create_text(world: esper.World, text_cfg: dict, text: str | None = None) -> int:
    entity = world.create_entity()
    world.add_component(entity, CText(
        text if text is not None else text_cfg.get("text", ""),
        text_cfg["font"], text_cfg["size"], _color(text_cfg["color"]),
        _vec(text_cfg["pos"]), text_cfg.get("align", "left")))
    if "field" in text_cfg:
        world.add_component(entity, CHudField(text_cfg["field"],
                                              text_cfg.get("fmt", "{}")))
    return entity


def create_input_player(world: esper.World, input_cfg: dict) -> None:
    """Crea una entidad por cada binding declarado en input.json (patron Command)."""
    for action in input_cfg["actions"]:
        device = InputDevice[action["device"]]
        if device == InputDevice.KEYBOARD:
            codes = [pygame.key.key_code(name) for name in action["keys"]]
        else:
            codes = action["buttons"]
        for code in codes:
            entity = world.create_entity()
            world.add_component(entity, CInputCommand(action["name"], code, device))


def create_wave(world: esper.World, wave_cfg: dict, enemies_cfg: dict,
                humanoid_cfg: dict, play_rect: pygame.Rect, world_width: float,
                create_humanoids: bool) -> int:
    """Puebla el planeta: astronautas en la superficie y Landers entrando por arriba."""
    humanoids = 0
    if create_humanoids:
        for i in range(wave_cfg["humanoids"]):
            x = (i + 0.5) * world_width / wave_cfg["humanoids"]
            create_humanoid(world, pygame.Vector2(x, play_rect.bottom), humanoid_cfg)
            humanoids += 1
    lander_cfg = enemies_cfg["Lander"]
    for _ in range(wave_cfg["landers"]):
        x = random.uniform(0, world_width)
        descend_until_y = random.uniform(play_rect.y + play_rect.height * 0.25,
                                         play_rect.y + play_rect.height * 0.6)
        create_lander(world, pygame.Vector2(x, play_rect.y), lander_cfg, descend_until_y)
    return humanoids
