import pickle
import socket
import pygame
from pygame.locals import *
from sys import exit
from game.tools import *
from client.player_drawer import draw
from server.data_packets import *
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

PRIVATE_PORT = -1

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'JOIN_GAME')
    data = s.recv(1024)
    if data != b"SERVER_FULL":
        print("private port ", data)
        PRIVATE_PORT = int(data)
        print(PRIVATE_PORT)
    else:
        print(data)

screen_size = (1280//2, 720//2)
screen_center = (screen_size[0]/2, screen_size[1]/2)

pygame.init()
screen = pygame.display.set_mode((screen_size[0], screen_size[1]), 0, 32)

mouse_pos = screen_center
angle = 0
direction = (0, 0)
clock = pygame.time.Clock()
player: None or PlayerWithSurfaceAndTrack = None
other_players = {}
data_to_send = pickle.dumps(((0, 0), 0))

if PRIVATE_PORT > 0:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PRIVATE_PORT))
        while True:

            dt = clock.tick(60)

            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == MOUSEMOTION:  # if mouse click then coordinate array will append x,y tuple
                    mouse_pos = event.pos
                    angle = get_angle(screen_center, mouse_pos)
                    direction = normalise_vector(get_vector(screen_center, mouse_pos))

                    data_to_send = pickle.dumps((direction, dt))

                    # s.sendall(bytearray(('PING ' + str(PRIVATE_PORT)), encoding='utf8'))
                    # print("private port ", data)
            s.send(data_to_send)

            data = s.recv(1024)
            description: TypeOfUpdate = pickle.loads(data)
            s.send(b'OK')
            data = s.recv(description.length_of_data)
            game_state = pickle.loads(data)
            if description.is_only_track_update:
                player.update_track(game_state)
            else:
                player = game_state
            s.send(b'OK')

            data = s.recv(1024)
            num_of_other_players = int(data)
            # print("Liczba pozostałych graczy: ", num_of_other_players)
            s.send(b'OK')
            updated_keys = []
            for i in range(num_of_other_players):
                data = s.recv(1024)
                description: TypeOfUpdate = pickle.loads(data)
                s.send(b'OK')
                data = s.recv(description.length_of_data)
                game_state = pickle.loads(data)
                # print(description.is_only_track_update)
                updated_keys.append(game_state.port)
                if description.is_only_track_update:
                    other_players[game_state.port].update_track(game_state)
                else:
                    other_players[game_state.port] = game_state
                s.send(b'OK')
            keys_to_remove = []
            for key in other_players.keys():
                if key not in updated_keys:
                    keys_to_remove.append(key)
            for key in keys_to_remove:
                other_players.pop(key, None)

            screen.fill((255, 255, 255))
            screen.lock()
            draw(screen, screen_center, player)
            screen.unlock()
            pygame.display.update()

