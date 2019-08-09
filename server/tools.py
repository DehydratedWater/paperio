import math


def init_surface():
    starting_surface = []
    points = 40
    radius = 50
    for i in range(points):
        x = math.cos(2 * math.pi / points * i) * radius
        y = math.sin(2 * math.pi / points * i) * radius
        starting_surface.append((x, y))
    starting_surface.reverse()
    return starting_surface
