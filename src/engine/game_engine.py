"""Motor del juego: patron Game Loop + gestor de escenas."""
import asyncio
import json

import pygame

from src.engine.scenes.game_over_scene import GameOverScene
from src.engine.scenes.menu_scene import MenuScene
from src.engine.scenes.play_scene import PlayScene
from src.engine.service_locator import preload_assets

_CFG = "assets/cfg/"


class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()

        pygame.init()
        self._init_mixer()
        pygame.font.init()
        pygame.display.set_caption(self.window_cfg["title"])
        self.screen = pygame.display.set_mode(
            (self.window_cfg["size"]["w"], self.window_cfg["size"]["h"]),
            pygame.SCALED | pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.framerate = self.window_cfg["framerate"]
        self.bg_color = pygame.Color(self.window_cfg["bg_color"]["r"],
                                     self.window_cfg["bg_color"]["g"],
                                     self.window_cfg["bg_color"]["b"])
        self.is_running = False
        self.delta_time = 0.0
        # Resultados de la ultima partida, para que GAME_OVER muestre el puntaje
        self.last_results: dict[str, int] = {}

        preload_assets(self.assets_cfg)
        self._scenes: dict[str, object] = {}
        self._current_scene = None
        self._scene_to_switch: str | None = None

    # -------------------------------------------------------------- configuracion
    def _load_config_files(self) -> None:
        """Todo numero ajustable del juego vive en assets/cfg/*.json."""
        self.window_cfg = self._load("window.json")
        self.layout_cfg = self.window_cfg["layout"]
        self.assets_cfg = self._load("assets.json")
        self.input_cfg = self._load("input.json")
        self.player_cfg = self._load("player.json")
        self.laser_cfg = self._load("laser.json")
        self.enemies_cfg = self._load("enemies.json")
        self.humanoid_cfg = self._load("humanoid.json")
        self.explosion_cfg = self._load("explosion.json")
        self.score_cfg = self._load("score.json")
        self.scenes_cfg = self._load("scenes.json")
        self.menu_cfg = self.scenes_cfg["menu"]
        self.game_over_cfg = self.scenes_cfg["game_over"]

    @staticmethod
    def _load(name: str) -> dict:
        with open(_CFG + name, encoding="utf-8") as cfg_file:
            return json.load(cfg_file)

    @staticmethod
    def _init_mixer() -> None:
        """El audio puede no estar disponible (web o maquina sin tarjeta); no es fatal."""
        try:
            pygame.mixer.init()
        except pygame.error:
            pass

    # ------------------------------------------------------------------- escenas
    def _build_scene(self, name: str):
        scene_cfg = self.scenes_cfg["scenes"][name]
        kind = scene_cfg["type"]
        if kind == "MENU":
            return MenuScene(self)
        if kind == "GAME_OVER":
            return GameOverScene(self)
        if kind == "PLAY":
            with open(scene_cfg["level"], encoding="utf-8") as level_file:
                return PlayScene(self, json.load(level_file))
        raise ValueError(f"Tipo de escena desconocido: {kind}")

    def switch_scene(self, name: str) -> None:
        """Pide el cambio de escena; se aplica al final del frame actual."""
        self._scene_to_switch = name

    def _apply_scene_switch(self) -> None:
        name = self._scene_to_switch
        self._scene_to_switch = None
        if self._current_scene is not None:
            self._current_scene.clean()
        if name not in self._scenes:
            self._scenes[name] = self._build_scene(name)
        self._current_scene = self._scenes[name]
        self._current_scene.create()

    # ----------------------------------------------------------------- game loop
    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            # Cede el control al navegador: obligatorio para la exportacion con pygbag
            await asyncio.sleep(0)
        self._clean()

    def _create(self) -> None:
        self.switch_scene(self.scenes_cfg["initial_scene"])
        self._apply_scene_switch()

    def _calculate_time(self) -> None:
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            else:
                self._current_scene.process_events(event)

    def _update(self) -> None:
        self._current_scene.update(self.delta_time)
        if self._scene_to_switch is not None:
            self._apply_scene_switch()

    def _draw(self) -> None:
        self._current_scene.draw(self.screen)
        pygame.display.flip()

    def _clean(self) -> None:
        if self._current_scene is not None:
            self._current_scene.clean()
        pygame.quit()
