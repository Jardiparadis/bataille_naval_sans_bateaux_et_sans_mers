from Soldier import Soldier
from Player import Player

""" def main():
    
if __name__ == 'main':
    main() """

# shape = (32,32)
player1 = Player()
player2 = Player()

for i in range(5):
    soldier = Soldier(f"soldier{+i+1}", 10, 10, 1, i+1)
    player1.soldier_list.append(soldier)
    print("p1:"+player1.soldier_list[i].name)

for i in range(5):
    soldier = Soldier(f"soldier{+i+1}", 10, 10, 1, i+1)
    player2.soldier_list.append(soldier)
    print("p2:"+player2.soldier_list[i].name)

# def display_board(soldier_list1, soldier_list2):
#     for y in range(shape[0]):
#         for x in range(shape[1]):
#             print("| ", end="")
#             for soldier in range(len(soldier_list1)):
#                 if soldier.x == shape.x and soldier.y == shape.y:
#                     print("X")
#             for soldier in range(len(soldier_list2)):
#                 if soldier.x == shape.x and soldier.y == shape.y:
#                     print("X")
#         print("\n")

player1.soldier_list[1].add_attack()
print(player1.soldier_list[1].attack)
player1.soldier_list[1].fight(player2.soldier_list[3])
# display_board(player1.soldier_list, player2.soldier_list)
player1.add_attack_to_soldier(player1.soldier_list[3])
player1.add_attack_to_soldier(player1.soldier_list[2])
player1.add_attack_to_soldier(player1.soldier_list[4])
player2.add_attack_to_soldier(player2.soldier_list[3])
player2.add_attack_to_soldier(player2.soldier_list[2])
player2.add_attack_to_soldier(player2.soldier_list[4])