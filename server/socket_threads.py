import pickle
import socket
import time
import threading
from server.game_server import *
from server.client import *
from server.player import *

game = Game()


def start_main_socket(dict_of_clients, host, port, free_ports, taken_ports):
    print("Free ports: ", free_ports)
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            print("Waiting for new players..")
            s.bind((host, port))
            s.listen()
            conn, addr = s.accept()

            with conn:
                print('Connected by', addr)
                data = conn.recv(1024)
                if not data:
                    break
                if len(free_ports) == 0 and data == b"JOIN_GAME":
                    print("Server is full..")
                    conn.send(b"SERVER_FULL")
                    s.close()
                    continue

                port_for_new_player = free_ports.pop()
                taken_ports.add(port_for_new_player)
                game.add_new_player(port_for_new_player, Player(port_for_new_player,
                                                                [r.randint(-100, 100), r.randint(-100, 100)], 0))
                conn.send(bytearray(str(port_for_new_player), encoding='utf8'))
                s.close()
                print("Dodawanie nowego gracza")

                thread_of_new_player = threading.Thread(target=start_listening_on_socket,
                                                        args=(dict_of_clients, host, port_for_new_player,
                                                              free_ports, taken_ports))
                dict_of_clients[port_for_new_player] = Client(port_for_new_player, host, thread_of_new_player)
                print("Dodano nowego gracza")
                print("Free ports: ", free_ports)


def start_listening_on_socket(dict_of_clients, host, port, free_ports, taken_ports):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))

            print("Listening on ", port)
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    ((x, y), dt) = pickle.loads(data)
                    # print(x, y)
                    game.update_player(port, x, y, dt)

                    description, game_state_to_send = game.get_pickled_state_with_description(port, port)
                    conn.send(description)
                    data = conn.recv(1024)
                    conn.send(game_state_to_send)
                    data = conn.recv(1024)

                    other_players = game.get_pickled_list_of_other_players(port)
                    conn.send(bytearray(str(len(other_players)), encoding='utf8'))
                    data = conn.recv(1024)
                    for player in other_players:
                        conn.send(player[0])
                        data = conn.recv(1024)
                        conn.send(player[1])
                        data = conn.recv(1024)

                    time.sleep(0.001)
    except Exception as e:
        print("error: ", e.with_traceback())
        print("Rozłączono gracza ", port)
        dict_of_clients.pop(port, None)
        game.remove_player(port)
        taken_ports.remove(port)
        free_ports.add(port)
        print("Free ports: ", free_ports)

    print("Rozłączono gracza ", port)
    dict_of_clients.pop(port, None)
    game.remove_player(port)
    taken_ports.remove(port)
    free_ports.add(port)
    print("Free ports: ", free_ports)