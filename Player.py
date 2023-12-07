from Soldier import Soldier

class Player:

    def __init__(self):
        self.soldier_list = []
        self.start_side = ""
        self.nb_point = 60

    def add_attack_to_soldier(self, soldier: Soldier):
        soldier.add_attack()
        self.nb_point -= 1
        print(self.nb_point)

    def add_defense_to_soldier(self, soldier: Soldier):
        soldier.add_defense()
        self.nb_point -= 1
        print(self.nb_point)