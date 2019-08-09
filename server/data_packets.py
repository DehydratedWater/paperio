
class TypeOfUpdate:
    def __init__(self, length_of_data, is_only_track_update = True):
        self.is_only_track_update = is_only_track_update
        self.length_of_data = length_of_data


class PlayerWithTrack:
    def __init__(self, position, rotation, player_color, surface_color, track, port):
        self.position = position
        self.rotation = rotation
        self.player_color = player_color
        self.surface_color = surface_color
        self.track = track
        self.port = port


class PlayerWithSurfaceAndTrack(PlayerWithTrack):
    def __init__(self, position, rotation, player_color, surface_color, track, surface, port):
        super().__init__(position, rotation, player_color, surface_color, track, port)
        self.surface = surface

    def update_track(self, player_with_track):
        self.position = player_with_track.position
        self.rotation = player_with_track.rotation
        self.player_color = player_with_track.player_color
        self.surface_color = player_with_track.surface_color
        self.track = player_with_track.track

