import random as r
from server.tools import *
from game.tools import *


class Player:

    def __init__(self, port, position, rotation):
        self.position = position
        self.rotation = rotation
        self.port = port
        self.player_color = (r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
        self.surface_color = (int(self.player_color[0] * 0.8),
                              int(self.player_color[1] * 0.8), int(self.player_color[1] * 0.8))
        self.track = []
        self.surface = init_surface()
        self.last_direction = (0, 0)
        self.angular_velocity = 2 * math.pi / 1000
        self.speed = 0.1
        self.was_surface_updated = False
        self.needs_update_from_ports = set()


    def move_player(self, x, y, dt):
        direction = (x, y)
        direction = normalise_vector(direction)
        x = math.cos(self.rotation)
        y = math.sin(self.rotation)
        left_right = is_point_on_the_left(direction, multiply(direction, 2), (x, y))
        # print(left_right)

        self.last_direction = (x, y)
        if left_right > 0:
            self.rotation -= self.angular_velocity * dt
        elif left_right < 0:
            self.rotation += self.angular_velocity * dt

        x = math.cos(self.rotation)
        y = math.sin(self.rotation)
        self.position[0] -= x * self.speed * dt
        self.position[1] -= y * self.speed * dt

    def check_collisions(self):
        new_track_point = (-self.position[0], -self.position[1])

        if len(self.track) > 0 and get_distance_between_points(new_track_point, self.track[-1]) > 6:
            self.track.append(new_track_point)
        elif len(self.track) == 0:
            self.track.append(new_track_point)




