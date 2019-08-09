import random as r

import pygame
import pygame.gfxdraw

from game.tools import *



def calculate_position(points, position, screen_center):
    new_points = []
    for p in points:
        new_points.append((p[0] + position[0] + screen_center[0], p[1] + position[1] + screen_center[1]))
    return new_points


class Player(object):
    def __init__(self):
        self.player_color = (r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
        self.surface_color = (int(self.player_color[0] * 0.8),
                              int(self.player_color[1] * 0.8), int(self.player_color[1] * 0.8))
        self._points = []
        self.surface_points = []
        self.init_surface()
        self.position = [0, 0]
        self.player_rotation = 0
        self.angular_velocity = 2*math.pi/1000
        self.speed = 0.1
        self.track = []
        self.track_state = []
        self.player_rect = []
        self.player_inside = True
        self.was_last_inside = True
        self.num_of_crossings = 0
        self.last_direction = (0, 0)

    def reset(self):
        self.player_color = (r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
        self.surface_color = (int(self.player_color[0] * 0.9),
                              int(self.player_color[1] * 0.9), int(self.player_color[1] * 0.9))
        self._points = []
        self.surface_points = []
        self.player_rotation = 0.5 * math.pi
        self.init_surface()
        self.position = [0, 0]
        self.player_rotation = 0
        self.track = []
        self.track_state = []
        self.player_rect = []
        self.player_inside = True
        self.was_last_inside = True
        self.num_of_crossings = 0
        self.last_direction = (1, 0)

    def init_surface(self):
        points = 40
        radius = 50
        for i in range(points):
            x = math.cos(2 * math.pi / points * i) * radius
            y = math.sin(2 * math.pi / points * i) * radius
            self.surface_points.append((x, y))
        self.surface_points.reverse()

    def draw(self, screen, screen_center):
        self._draw_surface(screen, screen_center)
        self.player_inside = self._check_collision_with_surface(screen, screen_center)
        self._draw_player(screen, screen_center)
        self._draw_track(screen, screen_center)
        self._draw_helping_surface(screen, screen_center)

    def move_player(self, angle, direction, dt):
        # print(angle)
        x = math.cos(self.player_rotation)
        y = math.sin(self.player_rotation)
        left_right = is_point_on_the_left(direction, multiply(direction, 2), (x, y))
        print(left_right)

        self.last_direction = (x, y)
        if left_right > 0:
            self.player_rotation -= self.angular_velocity * dt
        elif left_right < 0:
            self.player_rotation += self.angular_velocity * dt

        x = math.cos(self.player_rotation)
        y = math.sin(self.player_rotation)
        self.position[0] -= x * self.speed * dt
        self.position[1] -= y * self.speed * dt

    def check_collisions(self):
        new_track_point = (-self.position[0], -self.position[1])

        if len(self.track) > 0 and get_distance_between_points(new_track_point, self.track[-1]) > 6:
            self.track.append(new_track_point)
            self.track_state.append(self.player_inside)
        elif len(self.track) == 0:
            self.track.append(new_track_point)
            self.track_state.append(self.player_inside)
        p = self.check_collision_with_track()
        if p is not None and not self.player_inside:
            self.reset()

        if self.was_last_inside != self.player_inside:
            self.was_last_inside = self.player_inside
            self.num_of_crossings += 1
            if self.num_of_crossings == 2:
                self.update_surface()
                self.num_of_crossings = 0

    def _draw_surface(self, screen, screen_center):
        if len(self.surface_points) > 1:
            pygame.gfxdraw.filled_polygon(screen, calculate_position(self.surface_points, self.position, screen_center),
                                          self.surface_color)

    def _draw_helping_surface(self, screen, screen_center):
        if len(self.surface_points) > 1:
            pygame.draw.polygon(screen, (255, 0, 0),
                                calculate_position(self.surface_points, self.position, screen_center), 1)

    def _draw_player(self, screen, screen_center):
        points = 4
        radius = 10
        self.player_rect = []
        for i in range(points):
            x = math.cos(2 * math.pi / points * i + 0.25 * math.pi + self.player_rotation) * radius
            y = math.sin(2 * math.pi / points * i + 0.25 * math.pi + self.player_rotation) * radius
            self.player_rect.append((x, y))
        pygame.draw.polygon(screen, self.player_color,
                            calculate_position(self.player_rect, (0, 0), screen_center), 6)

    def _draw_track(self, screen, screen_center):
        # print(self.track)
        if len(self.track) > 1:
            pygame.draw.lines(screen, self.surface_color, False,
                              calculate_position(self.track, self.position, screen_center), 3)

    def check_collision_with_track(self):
        if len(self.track) < 6:
            return None
        for p in self.track[:-4]:
            dist = get_distance_between_points((p[0] + self.position[0], p[1] + self.position[1]), (0, 0))
            # print(dist)
            if dist < 5:
                return p
        return None

    def _check_collision_with_surface(self, screen, screen_center):
        # print(screen_center)
        screen_size = (int(screen_center[0]), int(screen_center[1]))
        # print(screen.get_at(screen_size)[:3], self.surface_color)
        return screen.get_at(screen_size)[0] == self.surface_color[0] and \
               screen.get_at(screen_size)[1] == self.surface_color[1] \
               and screen.get_at(screen_size)[2] == self.surface_color[2]

    def update_surface(self):
        if len(self.track) < 3:
            self.track = []
            self.track_state = []
            return

        indexes_start_end = [0, len(self.track) - 1]

        for i in range(len(self.track)):
            if self.track_state[i]:
                indexes_start_end[0] = i
            else:
                break

        new_surface = self.track[indexes_start_end[0]:indexes_start_end[1]]

        if len(new_surface) < 3:
            self.track = []
            self.track_state = []
            return

        was_polygon_clockwise = is_polygon_clockwise(new_surface)

        print(is_polygon_clockwise(self.surface_points), is_polygon_clockwise(new_surface))

        if not was_polygon_clockwise:
            new_surface.reverse()

        print(is_polygon_clockwise(self.surface_points), is_polygon_clockwise(new_surface))

        closest_points = [0, 0]
        distances = [999999, 999999]
        for i in range(len(self.surface_points)):
            dist_1 = get_distance_between_points(self.surface_points[i], new_surface[0])
            dist_2 = get_distance_between_points(self.surface_points[i], new_surface[-1])
            if distances[0] > dist_1:
                closest_points[0] = i
                distances[0] = dist_1
            if distances[1] > dist_2:
                closest_points[1] = i
                distances[1] = dist_2

        if closest_points[0] == closest_points[1]:
            closest_points[0] -= 1

        ind_1 = [closest_points[1] - 1]
        ind_2 = [closest_points[1]]
        ind_3 = [closest_points[1] + 1]
        if ind_3[0] >= len(self.surface_points):
            ind_3[0] = 0

        pt_1 = self.surface_points[ind_1[0]]
        pt_2 = self.surface_points[ind_2[0]]
        pt_3 = self.surface_points[ind_3[0]]

        print(ind_1, ind_2, ind_3)
        last = new_surface[-1]
        pre_last = new_surface[-2]
        print(is_point_on_the_left(pre_last, last, pt_1), is_point_on_the_left(pre_last, last, pt_2),
              is_point_on_the_left(pre_last, last, pt_3))

        new_surface = new_surface[1:-1]
        test_surface = new_surface[1:-1]
        index_start = [ind_2[0]]
        while index_start[0] != closest_points[0]:
            point_to_add = self.surface_points[index_start[0]]
            # print(point_to_add)
            test_surface.append(point_to_add)
            index_start[0] += 1
            if index_start[0] >= len(self.surface_points):
                index_start[0] = 0

        if not is_polygon_clockwise(test_surface):
            print("WKLĘSŁY CASE UWAGAAA XDDD")
            test_surface = new_surface[1:-1]
            index_start = [ind_2[0]]
            while index_start[0] != closest_points[0]:
                point_to_add = self.surface_points[index_start[0]]
                # print(point_to_add)
                test_surface.append(point_to_add)
                index_start[0] -= 1
                if index_start[0] < 0:
                    index_start[0] = len(self.surface_points)-1
            if not is_polygon_clockwise(test_surface):
                test_surface.reverse()
            self.surface_points = test_surface
        else:
            if not is_polygon_clockwise(test_surface):
                test_surface.reverse()
            self.surface_points = test_surface

        self.track = []
        self.track_state = []