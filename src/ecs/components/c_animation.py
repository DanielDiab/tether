class AnimationData:
    """Datos de una animacion: cuadros [start, end] de la textura a `framerate` cuadros/s."""

    def __init__(self, name: str, start: int, end: int, framerate: float,
                 number_frames: int) -> None:
        if not 0 <= start <= end < number_frames:
            raise ValueError(f"Animacion '{name}': se requiere 0 <= start <= end < "
                             f"number_frames ({start}, {end}, {number_frames})")
        if framerate <= 0:
            raise ValueError(f"Animacion '{name}': framerate debe ser mayor que cero")
        self.name = name
        self.start = start
        self.end = end
        self.framerate_time = 1.0 / framerate


class CAnimation:
    """Controla el flujo de las animaciones de una textura con `number_frames` cuadros."""

    def __init__(self, number_frames: int, animations: list[AnimationData],
                 initial_anim: str) -> None:
        self.number_frames = number_frames
        self.animations = {anim.name: anim for anim in animations}
        self.curr_anim = initial_anim
        anim = self.animations[initial_anim]
        self.curr_frame = anim.start
        self.curr_anim_time = anim.framerate_time
        self.finished = False
