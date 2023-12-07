class Soldier:

    def __init__(self, name, attack, defence, x, y):
        self.name = name
        self.attack = attack
        self.defence = defence
        self.x = x
        self.y = y
    
    def add_attack(self):
        if self.attack < 20:
            self.attack += 1
            return 1

    def add_defense(self):
        if self.attack < 20:
            self.attack += 1


    def fight(self, enemy):
        if self.attack > enemy.attack :
            print(f"{self.name} wins and {enemy.name} loses")
        else:
            print(f"{enemy.name} wins and {self.name} loses")

    # def move():
    #     pass
