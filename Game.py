from MapGenerator import MapGenerator, BoxType
from Player import Player
from Soldier import Soldier
import random

MAP_SHAPE = (32, 32)
NB_SOLDIERS = 6


class Game:
    def __init__(self) -> None:
        self.players: list[Player] = []
        self.seed = random.randint(0,1000)
        self.mapGenerator = MapGenerator(MAP_SHAPE, self.seed)
        #self.images = images

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

    def move_soldier(self, soldier: Soldier, pos_x: int, pos_y: int) -> bool:
        # Check if pos is out of bounds
        if pos_x < 0 or pos_y < 0 or pos_x > (MAP_SHAPE[0] - 1) or pos_y > (MAP_SHAPE[0] - 1):
            print(f"Soldier cannot go to ({pos_x},{pos_y}): out of bound")
            return False
        
        # Check if pos is a valid cell
        if self.mapGenerator.map[pos_y][pos_x] == BoxType.Water:
            print(f"Soldier cannot go to ({pos_x},{pos_y}): it is water")
            return False
        
        # Check if pos is next to soldier
        if abs(soldier.x - pos_x) in (0, 1) and abs(soldier.y - pos_y) in (0, 1):
            if abs(soldier.x - pos_x) + abs(soldier.y - pos_y) > 0:
                return True
        
        # If not next to the soldier
        print(f"Soldier cannot go to ({pos_x},{pos_y}): it is not located next to the soldier")
        return False
