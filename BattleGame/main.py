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
    while (user_choice < 1) && (user_choice > max_choice):
        print "Invalid choice"
        user_choice = raw_input()

    return user_choice

def get_battle_choice():
    print("------");
    print("\t# " + enemy.name + " appears! #\n");
    print("\tYour HP is: " + playerHealth)
    print("\t" + enemy.name + "'s HP: " + enemy.health)
    print("\n\tWhat would you like to do?")
    print("\t1. Attack")
    print("\t2. Drink health potion")
    print("\t3. Drink strength potion")
    print("\t4. Run!")
    print("------")

    return get_valid_input(4)

def get_idle_choice():
    print("------")
    print("\t1. Fight")
    print("\t2. Visit the shop")
    print("\t3. Sacrifice Illbane...")
    print("\t4. Exit dungeon")
    print("------")

    return get_valid_input(4)

def run_game():
    player = Character("The player", 100, 30, 20, [])
    enemies = init_enemies()
    while True:
        if (get_idle_choice() == 1):



if __name__ == "__main__":
    run_game()
