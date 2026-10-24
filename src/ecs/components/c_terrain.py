class CTerrain:
    """Perfil del terreno del planeta.

    `points` son vertices (x, y) en coordenadas de mundo, ordenados por x y cerrando
    el ciclo (el ultimo x coincide con el ancho del mundo) para que el scroll sea
    continuo al dar la vuelta al planeta.
    """

    def __init__(self, points: list[tuple[float, float]], world_width: float) -> None:
        self.points = points
        self.world_width = world_width

    def height_at(self, world_x: float) -> float:
        """Interpola la altura del terreno en una x de mundo."""
        x = world_x % self.world_width
        points = self.points
        for i in range(len(points) - 1):
            x0, y0 = points[i]
            x1, y1 = points[i + 1]
            if x0 <= x <= x1:
                if x1 == x0:
                    return y0
                t = (x - x0) / (x1 - x0)
                return y0 + (y1 - y0) * t
        return points[-1][1]
