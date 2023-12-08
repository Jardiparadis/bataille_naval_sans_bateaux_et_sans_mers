from MapGenerator import MapGenerator
from Player import Player
import random

MAP_SHAPE = (32, 32)
NB_SOLDIERS = 6


class Game:
    def __init__(self) -> None:
        self.players: list[Player] = []
        self.seed = random.randint(0,1000)
        self.mapGenerator = MapGenerator(MAP_SHAPE, self.seed)

    def add_player(self):
        if len(self.players) > 2:
            return
        player = Player()
        self.players.append(player)
        # Initialize soldiers
        for i in range(0, 6):
            player.add_soldier()

    def place_soldiers_to_initial_pos(self):
        i = 0
        for soldier in self.players[0].soldier_list:
            soldier.y = 31
            soldier.x = 13 + i
            i += 1
        i = 0
        for soldier in self.players[1].soldier_list:
            soldier.y = 0
            soldier.x = 13 + i
            i += 1
