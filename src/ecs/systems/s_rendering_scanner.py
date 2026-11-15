import esper
import pygame

from src.ecs.components.c_camera import CCamera
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_terrain import CTerrain
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_humanoid import CTagHumanoid
from src.ecs.components.tags.c_tag_lander import CTagLander
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_rendering_scanner(world: esper.World, screen: pygame.Surface, c_cam: CCamera,
                             world_width: float, play_rect: pygame.Rect,
                             scanner_cfg: dict) -> None:
    """Radar de largo alcance: comprime TODO el planeta en una franja superior.

    Es la pieza central del juego: muestra enemigos y astronautas fuera
    de pantalla, y un marco con la porcion del mundo que se esta viendo.
    """
    rect = pygame.Rect(scanner_cfg["x"], scanner_cfg["y"],
                       scanner_cfg["w"], scanner_cfg["h"])
    colors = scanner_cfg["colors"]
    pygame.draw.rect(screen, pygame.Color(*colors["frame"]), rect, width=1)

    inner = rect.inflate(-2, -2)
    scale_x = inner.width / world_width
    scale_y = inner.height / play_rect.height

    def to_scanner(world_x: float, world_y: float) -> tuple[int, int]:
        sx = inner.x + (world_x % world_width) * scale_x
        sy = inner.y + (world_y - play_rect.y) * scale_y
        return int(sx), int(sy)

    for _, c_terrain in world.get_component(CTerrain):
        pts = [to_scanner(x, y) for x, y in c_terrain.points]
        if len(pts) > 1:
            pygame.draw.lines(screen, pygame.Color(*colors["terrain"]), False, pts)

    for tag, key in ((CTagHumanoid, "humanoid"), (CTagLander, "lander"),
                     (CTagPlayer, "player")):
        color = pygame.Color(*colors[key])
        for _, (c_t, _c_s, _tag) in world.get_components(CTransform, CSurface, tag):
            pygame.draw.rect(screen, color, (*to_scanner(c_t.pos.x, c_t.pos.y), 2, 2))

    # Marco de la region visible, que se parte en dos si cruza la costura del mundo
    view_w = max(2, int(play_rect.width * scale_x))
    view_x = inner.x + (c_cam.rect.x % world_width) * scale_x
    view = pygame.Color(*colors["view"])
    pygame.draw.rect(screen, view, (int(view_x), inner.y, view_w, inner.height), width=1)
    if view_x + view_w > inner.right:
        wrapped = int(view_x - inner.width)
        pygame.draw.rect(screen, view, (wrapped, inner.y, view_w, inner.height), width=1)
