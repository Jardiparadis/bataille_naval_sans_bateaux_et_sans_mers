class Soldier:

    def __init__(self, img="", name="", attack=1, defence=1, x=0, y=0):
        self.name = name
        self.attack = attack
        self.defence = defence
        self.x = x
        self.y = y
        self.img = img
    
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


    def display(self, screen):
        screen.blit(self.img, (self.x * 29, self.y * 29))

    # def move():
    #     pass
