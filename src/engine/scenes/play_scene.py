"""Escena de juego: el planeta, la nave, los astronautas y los Landers."""
import pygame

from src.create.prefab_creator import (create_camera, create_game_state,
                                       create_input_player, create_laser, create_player,
                                       create_terrain, create_text, create_wave)
from src.ecs.components.c_camera import CCamera
from src.ecs.components.c_game_state import CGameState
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_lander import CTagLander
from src.ecs.components.tags.c_tag_laser import CTagLaser
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_camera import system_camera
from src.ecs.systems.s_collision_laser_humanoid import system_collision_laser_humanoid
from src.ecs.systems.s_collision_laser_lander import system_collision_laser_lander
from src.ecs.systems.s_collision_player_humanoid import system_collision_player_humanoid
from src.ecs.systems.s_collision_player_lander import system_collision_player_lander
from src.ecs.systems.s_explosion_kill import system_explosion_kill
from src.ecs.systems.s_hud import system_hud
from src.ecs.systems.s_humanoid import system_humanoid
from src.ecs.systems.s_lander_state import system_lander_state
from src.ecs.systems.s_lifetime import system_lifetime
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_limits import system_player_limits
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_rendering_scanner import system_rendering_scanner
from src.ecs.systems.s_rendering_terrain import system_rendering_terrain
from src.ecs.systems.s_world_wrap import system_world_wrap
from src.engine.scenes.scene import Scene
from src.engine.world_math import world_to_screen_x

# Direccion en la que cada accion de movimiento empuja a la nave
_MOVE_ACTIONS = {
    "PLAYER_LEFT": pygame.Vector2(-1, 0),
    "PLAYER_RIGHT": pygame.Vector2(1, 0),
    "PLAYER_UP": pygame.Vector2(0, -1),
    "PLAYER_DOWN": pygame.Vector2(0, 1),
}


class PlayScene(Scene):
    def __init__(self, engine, level_cfg: dict) -> None:
        super().__init__(engine)
        self._level_cfg = level_cfg
        self._debug = False

    # --------------------------------------------------------------------- creacion
    def do_create(self) -> None:
        engine = self._engine
        self._world_width = float(self._level_cfg["world"]["width"])
        self._play_rect = pygame.Rect(0, engine.layout_cfg["play_area"]["y"],
                                      engine.window_cfg["size"]["w"],
                                      engine.layout_cfg["play_area"]["h"])
        self._respawn_pos = pygame.Vector2(self._level_cfg["player_spawn"]["x"],
                                           self._level_cfg["player_spawn"]["y"])

        create_game_state(self.ecs_world, self._level_cfg["game"])
        create_terrain(self.ecs_world, self._level_cfg["terrain"], self._play_rect,
                       self._world_width)
        self._camera_entity = create_camera(self.ecs_world, self._play_rect,
                                            self._level_cfg["camera"]["player_screen_x"])
        self._player_entity = create_player(self.ecs_world, engine.player_cfg,
                                            self._respawn_pos)
        self._player_c_t = self.ecs_world.component_for_entity(self._player_entity,
                                                               CTransform)
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity,
                                                               CVelocity)
        self._player_c_s = self.ecs_world.component_for_entity(self._player_entity,
                                                               CSurface)
        self._player_c_st = self.ecs_world.component_for_entity(self._player_entity,
                                                                CPlayerState)
        create_input_player(self.ecs_world, engine.input_cfg)
        for text_cfg in engine.layout_cfg["hud"]:
            create_text(self.ecs_world, text_cfg)
        self._c_state = self.ecs_world.get_component(CGameState)[0][1]
        self._c_camera = self.ecs_world.component_for_entity(self._camera_entity, CCamera)
        self._spawn_wave(first=True)

    def _spawn_wave(self, first: bool) -> None:
        wave_index = min(self._c_state.wave, len(self._level_cfg["waves"])) - 1
        wave_cfg = self._level_cfg["waves"][wave_index]
        humanoids = create_wave(self.ecs_world, wave_cfg, self._engine.enemies_cfg,
                                self._engine.humanoid_cfg, self._play_rect,
                                self._world_width, create_humanoids=first)
        if first:
            self._c_state.humanoids_alive = humanoids

    # ----------------------------------------------------------- acciones (Command)
    def do_action(self, c_input: CInputCommand) -> None:
        if c_input.name in _MOVE_ACTIONS:
            self._update_player_velocity()
        elif c_input.phase != CommandPhase.START:
            return
        elif c_input.name == "PLAYER_FIRE":
            self._fire()
        elif c_input.name == "GAME_PAUSE":
            self._c_state.paused = not self._c_state.paused
        elif c_input.name == "GAME_MENU":
            self.switch_scene("MENU")
        elif c_input.name == "DEBUG_COLLIDERS":
            self._debug = not self._debug
        elif c_input.name == "CHEAT_ADD_LIFE":
            self._c_state.lives += 1
        elif c_input.name == "CHEAT_NEXT_WAVE":
            self._clear_landers()

    def _update_player_velocity(self) -> None:
        # Una accion esta activa si cualquiera de sus teclas esta presionada, asi
        # pulsar flecha y WASD a la vez no duplica la velocidad
        active = {c.name for _, c in self.ecs_world.get_component(CInputCommand)
                  if c.phase == CommandPhase.START}
        direction = pygame.Vector2(0, 0)
        for name in active & _MOVE_ACTIONS.keys():
            direction += _MOVE_ACTIONS[name]
        self._player_c_v.vel = direction * self._engine.player_cfg["velocity"]

    def _fire(self) -> None:
        max_lasers = self._level_cfg["player_spawn"]["max_lasers"]
        if len(self.ecs_world.get_component(CTagLaser)) >= max_lasers:
            return
        create_laser(self.ecs_world, self._player_c_t.pos, self._player_c_s.area,
                     self._player_c_st.facing, self._engine.laser_cfg)

    def _clear_landers(self) -> None:
        for entity, _tag in self.ecs_world.get_component(CTagLander):
            self.ecs_world.delete_entity(entity)

    # ------------------------------------------------------------------ actualizacion
    def do_update(self, delta_time: float) -> None:
        if self._c_state.paused:
            return
        engine = self._engine
        system_lander_state(self.ecs_world, delta_time, self._play_rect,
                            self._world_width)
        system_movement(self.ecs_world, delta_time)
        system_world_wrap(self.ecs_world, self._world_width)
        system_player_limits(self.ecs_world, self._play_rect)
        system_humanoid(self.ecs_world, delta_time, self._play_rect, engine.humanoid_cfg)
        system_collision_laser_lander(self.ecs_world, self._world_width,
                                      engine.explosion_cfg, engine.score_cfg)
        system_collision_laser_humanoid(self.ecs_world, self._world_width,
                                        engine.explosion_cfg)
        system_collision_player_humanoid(self.ecs_world, self._world_width)
        system_collision_player_lander(self.ecs_world, self._player_entity,
                                       self._world_width, engine.explosion_cfg,
                                       engine.player_cfg, self._respawn_pos)
        system_lifetime(self.ecs_world, delta_time)
        system_player_state(self.ecs_world)
        system_animation(self.ecs_world, delta_time)
        system_blink(self.ecs_world, delta_time)
        system_explosion_kill(self.ecs_world)
        system_camera(self.ecs_world, self._player_entity, self._world_width)
        system_hud(self.ecs_world)
        self._check_progress()

    def _check_progress(self) -> None:
        if self._c_state.lives <= 0:
            self._engine.last_results = {"score": self._c_state.score,
                                         "wave": self._c_state.wave}
            self.switch_scene("GAME_OVER")
            return
        # Ola superada cuando no queda ningun Lander en el planeta
        if not self.ecs_world.get_component(CTagLander):
            self._c_state.wave += 1
            self._spawn_wave(first=False)

    # ------------------------------------------------------------------------ dibujo
    def do_draw(self, screen: pygame.Surface) -> None:
        engine = self._engine
        system_rendering_terrain(self.ecs_world, screen, self._c_camera, self._play_rect,
                                 pygame.Color(*engine.layout_cfg["terrain_color"]))
        system_rendering(self.ecs_world, screen, self._c_camera, self._world_width,
                         self._play_rect)
        system_rendering_scanner(self.ecs_world, screen, self._c_camera,
                                 self._world_width, self._play_rect,
                                 engine.layout_cfg["scanner"])
        if self._debug:
            self._draw_colliders(screen)

    def _draw_colliders(self, screen: pygame.Surface) -> None:
        """Ayuda de depuracion (tecla de DEBUG_COLLIDERS): dibuja las cajas de colision."""
        for _, (c_t, c_s) in self.ecs_world.get_components(CTransform, CSurface):
            screen_x = world_to_screen_x(c_t.pos.x, self._c_camera.rect.x,
                                         self._world_width, self._play_rect.width,
                                         c_s.area.w)
            if screen_x is None:
                continue
            pygame.draw.rect(screen, pygame.Color(255, 0, 255),
                             (self._play_rect.x + screen_x, c_t.pos.y,
                              c_s.area.w, c_s.area.h), width=1)
