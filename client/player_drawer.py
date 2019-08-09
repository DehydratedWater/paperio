from server.player import Player
import math
import pygame
import pygame.gfxdraw


def calculate_position(points, position, screen_center):
    new_points = []
    for p in points:
        new_points.append((p[0] + position[0] + screen_center[0], p[1] + position[1] + screen_center[1]))
    return new_points


def _draw_track(screen, screen_center, player):
    # print(self.track)
    if len(player.track) > 1:
        pygame.draw.lines(screen, player.surface_color, False,
                          calculate_position(player.track, player.position, screen_center), 3)


def _draw_helping_surface(screen, screen_center, player):
    if len(player.surface) > 1:
        pygame.draw.polygon(screen, (255, 0, 0),
                            calculate_position(player.surface, player.position, screen_center), 1)


def _draw_player(screen, screen_center, player):
    points = 4
    radius = 10
    player_rect = []
    for i in range(points):
        x = math.cos(2 * math.pi / points * i + 0.25 * math.pi + player.rotation) * radius
        y = math.sin(2 * math.pi / points * i + 0.25 * math.pi + player.rotation) * radius
        player_rect.append((x, y))
    pygame.draw.polygon(screen, player.player_color,
                        calculate_position(player_rect, (0, 0), screen_center), 6)


def _draw_surface(screen, screen_center, player):
    if len(player.surface) > 1:
        pygame.gfxdraw.filled_polygon(screen, calculate_position(player.surface, player.position, screen_center),
                                      player.surface_color)


def draw(screen, screen_center, player: Player):
    _draw_surface(screen, screen_center, player)
    _draw_player(screen, screen_center, player)
    _draw_track(screen, screen_center, player)
    _draw_helping_surface(screen, screen_center, player)


