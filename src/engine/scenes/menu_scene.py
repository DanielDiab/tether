import pygame

from src.create.prefab_creator import create_input_player, create_text
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.engine.scenes.scene import Scene


class MenuScene(Scene):
    """Pantalla de titulo. Solo tiene textos y entradas, nada de simulacion."""

    def do_create(self) -> None:
        create_input_player(self.ecs_world, self._engine.input_cfg)
        for text_cfg in self._engine.menu_cfg["texts"]:
            create_text(self.ecs_world, text_cfg)

    def do_action(self, c_input: CInputCommand) -> None:
        if c_input.phase != CommandPhase.START:
            return
        if c_input.name == "GAME_START":
            self.switch_scene(self._engine.menu_cfg["start_scene"])
        elif c_input.name == "GAME_MENU":
            self._engine.is_running = False

    def do_draw(self, screen: pygame.Surface) -> None:
        pass
