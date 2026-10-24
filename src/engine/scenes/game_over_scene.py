import pygame

from src.create.prefab_creator import create_input_player, create_text
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.engine.scenes.scene import Scene


class GameOverScene(Scene):
    """Resultado de la partida. El puntaje se lo deja la escena de juego en el motor."""

    def do_create(self) -> None:
        create_input_player(self.ecs_world, self._engine.input_cfg)
        for text_cfg in self._engine.game_over_cfg["texts"]:
            text = None
            if "field" in text_cfg:
                value = self._engine.last_results.get(text_cfg["field"], 0)
                text = text_cfg.get("fmt", "{}").format(value)
                text_cfg = {k: v for k, v in text_cfg.items() if k != "field"}
            create_text(self.ecs_world, text_cfg, text)

    def do_action(self, c_input: CInputCommand) -> None:
        if c_input.phase != CommandPhase.START:
            return
        if c_input.name in ("GAME_START", "GAME_MENU"):
            self.switch_scene(self._engine.game_over_cfg["next_scene"])

    def do_draw(self, screen: pygame.Surface) -> None:
        pass
