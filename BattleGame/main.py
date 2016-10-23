import random
from character import Character


def init_enemies():
    enemy_list = [
        Character("Kobold", random.randint(50, 150), 25, 10, []),
        Character("Kobold Warrior", random.randint(70, 220), 30, 20, []),
        Character("Kobold Archer", random.randint(90, 290), 40, 30, []),
        Character("Kobold Overseer", random.randint(150, 400), 50, 40, [])
    ]

    return enemy_list

def get_valid_input(max_choice):
    user_choice = raw_input()
    while (user_choice < 1) and (user_choice > max_choice):
        print "Invalid choice"
        user_choice = raw_input()

    return user_choice

def get_battle_choice(player, enemy):
    print("------");
    print("\t# " + enemy.name + " appears! #\n");
    print("\tYour HP is: " + player.health)
    print("\t" + enemy.name + "'s HP: " + enemy.health)
    print("\n\tWhat would you like to do?")
    print("\t1. Attack")
    print("\t2. Drink health potion")
    print("\t3. Drink strength potion")
    print("\t4. Run!")
    print("------")

    return int(get_valid_input(4))

def get_idle_choice():
    print("------------------------------")
    print("\t1. Fight")
    print("\t2. Visit the shop")
    print("\t3. Sacrifice Illbane...")
    print("\t4. Exit dungeon")
    print("------------------------------")

    return int(get_valid_input(4))

def fight_common_enemy(player, enemy=None):
    if (enemy == None):
        enemy = enemies[random.randint(len(enemies))]

    fighting = True
    print enemy.is_alive()
    print player.is_alive()

    while (fighting and enemy.is_alive() and player.is_alive()):
        battle_choice = get_battle_choice(player, enemy)
        if (battle_choice == 1):
            damage_dealt = random.randint(player.strength)
            damage_taken = random.randint(enemy.strength)
            enemy.health -= damage_dealt
            player.health -= damage_taken
            print("\t> You strike the " + enemy.name + " for " + str(damage_dealt) + " damage.")
            print("\t> You receive " + str(damage_taken) + " in retaliation!")
        if (battle_choice == 4):
            print("------")
            print("\tYou run away from the " + enemy.name + "!");
            print("------")
            fighting = false




def run_game():
    player = Character("The player", 100, 30, 20, [])
    enemies = init_enemies()
    while True:
        idle_choice = get_idle_choice()
        if (idle_choice == 1):
            fight_common_enemy(player)


if __name__ == "__main__":
    run_game()
