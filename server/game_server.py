import pickle
from server.player import *
from server.data_packets import *

class Game:
    def __init__(self):
        self.players = {}

    def add_new_player(self, port, player):
        self.players[port] = player

        for key in self.players.keys():
            player.needs_update_from_ports.add(key)
        for key in self.players.keys():
            self.players[key].needs_update_from_ports.add(port)
        for key in self.players.keys():
            print("Player: ",key," needs: ", self.players[key].needs_update_from_ports)

    def update_player(self, port, x, y, dt):
        self.players[port].move_player(x, y, dt)
        self.players[port].check_collisions()

    def remove_player(self, port):
        for key in self.players.keys():
            if port in self.players[key].needs_update_from_ports:
                self.players[key].needs_update_from_ports.remove(port)
        self.players.pop(port, None)

    def get_player_state_pickled(self, port):
        return pickle.dumps(self.players[port])

    def get_pickled_state_with_description(self, port, port_of_requester):
        player: Player = self.players[port]
        requester: Player = self.players[port_of_requester]
        if player.was_surface_updated:
            for key in self.players.keys():
                self.players[key].needs_update_from_ports.add(port)
            player.was_surface_updated = False

        if port in requester.needs_update_from_ports:
            requester.needs_update_from_ports.remove(port)

            # print("Aktualizowanie powierzchni")
            # print("Sending ",port," to player: ", port_of_requester, " still needs: ",
            #       self.players[port_of_requester].needs_update_from_ports)

            game_state = pickle.dumps(PlayerWithSurfaceAndTrack(player.position, player.rotation,
                                                                player.player_color, player.surface_color,
                                                                player.track, player.surface, port))
            length = len(game_state)
            description = pickle.dumps(TypeOfUpdate(length, False))
            return description, game_state
        else:
            # print("Player", port_of_requester, " = ", port, " Track ", "needs: ", requester.needs_update_from_ports)
            game_state = pickle.dumps(PlayerWithTrack(player.position, player.rotation, player.player_color,
                                                      player.surface_color, player.track, port))
            length = len(game_state)
            description = pickle.dumps(TypeOfUpdate(length, True))
            return description, game_state

    def get_pickled_list_of_other_players(self, port):
        list_ot_other_players = []
        for key in self.players.keys():
            if port == key:
                continue
            list_ot_other_players.append(self.get_pickled_state_with_description(key, port))

        return list_ot_other_players
