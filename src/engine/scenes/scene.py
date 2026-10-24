"""Patron Escena.

Cada escena es un mundo ECS independiente con su propio ciclo de vida. El motor solo
sabe crear, actualizar, dibujar y limpiar la escena activa, y cambiar a otra cuando la
escena lo pide. Asi el menu, el nivel y el game over no se conocen entre si.
"""
import esper
import pygame

from src.ecs.components.c_input_command import CInputCommand
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_rendering_text import system_rendering_text


class Scene:
    def __init__(self, engine) -> None:
        self.ecs_world = esper.World()
        self._engine = engine

    # ------------------------------------------------------------------ propiedades
    @property
    def engine(self):
        return self._engine

    @property
    def screen(self) -> pygame.Surface:
        return self._engine.screen

    # ------------------------------------------------- ciclo de vida (lo llama el motor)
    def create(self) -> None:
        self.do_create()

    def process_events(self, event: pygame.event.Event) -> None:
        system_input_player(self.ecs_world, event, self.do_action)

    def update(self, delta_time: float) -> None:
        self.do_update(delta_time)
        # No se usa world.process(), asi que las entidades muertas se limpian a mano
        self.ecs_world._clear_dead_entities()

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(self._engine.bg_color)
        self.do_draw(screen)
        system_rendering_text(self.ecs_world, screen)

    def clean(self) -> None:
        self.do_clean()
        self.ecs_world.clear_database()

    def switch_scene(self, name: str) -> None:
        self._engine.switch_scene(name)

    # --------------------------------------------------------- a implementar por escena
    def do_create(self) -> None:
        raise NotImplementedError

    def do_action(self, c_input: CInputCommand) -> None:
        pass

    def do_update(self, delta_time: float) -> None:
        pass

    def do_draw(self, screen: pygame.Surface) -> None:
        pass

    def do_clean(self) -> None:
        pass
