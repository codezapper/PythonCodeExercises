## Check difference between randint and randrange
## Move "enemies" variable so it's not global

import random
from character import Character
from shopitem import ShopItem
from potion import Potion

enemies = []
shop_items = []
potion_types = []

def init_enemies():
    enemy_list = [
        Character("Kobold", random.randint(50, 150), 25, 10, []),
        Character("Kobold Warrior", random.randint(70, 220), 30, 20, []),
        Character("Kobold Archer", random.randint(90, 290), 40, 30, []),
        Character("Kobold Overseer", random.randint(150, 400), 50, 40, [])
    ]

    return enemy_list

def init_shop():
    global shop_items, potion_types

    shop_items = [
        ShopItem("Silver Sword", 1000, 0, 100, 0),
        ShopItem("Steel Sword", 250, 0, 25, 0),
        ShopItem("Iron Helmet", 150, 10, 0, 0),
        ShopItem("Iron Chestplate", 200, 18, 0, 0),
        ShopItem("Iron Boots", 100, 8, 0, 0),
        ShopItem("Iron Gauntlets", 75, 5, 0, 0),
        ShopItem("Steel Helmet", 400, 5, 0, 0),
        ShopItem("Steel Chestplate", 600, 10, 10, 0),
        ShopItem("Steel Boots", 300, 10, 0, 0),
        ShopItem("Steel Gauntlets", 250, 7, 0, 0),
        ShopItem("Illbane", 2500, 0, 0, 1),
    ]
    potion_types = [
        Potion("Health Potion", 100, 30, 0, 50),
        Potion("Strength Potion", 500, 0, 2, 50)
    ]

def get_valid_input(max_choice):
    user_choice = raw_input()
    while (user_choice < 1) and (user_choice > max_choice):
        print "Invalid choice"
        user_choice = raw_input()

    return user_choice

def get_battle_choice(player, enemy):
    print("------");
    print("\tYour HP is: " + str(player.health))
    print("\t" + enemy.name + "'s HP: " + str(enemy.health))
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
    global enemies, potion_types

    if (enemy == None):
        enemy = enemies[random.randint(0, len(enemies)-1)]

    print("\t# " + enemy.name + " appears! #\n");

    fighting = True

    while (fighting and enemy.is_alive() and player.is_alive()):
        battle_choice = get_battle_choice(player, enemy)
        if (battle_choice == 1):
            damage_dealt = random.randint(0, player.strength - 1)
            damage_taken = random.randint(0, enemy.strength - 1)
            enemy.health -= damage_dealt
            player.health -= damage_taken
            print("\t> You strike the " + enemy.name + " for " + str(damage_dealt) + " damage.")
            print("\t> You receive " + str(damage_taken) + " in retaliation!")
        if (battle_choice == 2):
            if (potion_types[0] in player.inventory):
                player.health += potion_types[0].health_bonus
                print("You drink a health potion. You recover " + str(potion_types[0].health_bonus))
                if (player.health > player.initial_health):
                    player.health = player.initial_health
                player.inventory.remove(potion_types[0])
        if (battle_choice == 3):
            if (potion_types[1] in player.inventory):
                player.strength *= potion_types[1].strength_bonus
                print("You drink a strength potion. Your strength is now " + str(player.strength))
                player.inventory.remove(potion_types[1])
        if (battle_choice == 4):
            print("------")
            print("\tYou run away from the " + enemy.name + "!");
            print("------")
            fighting = False

    if (not player.is_alive()):
        print("\n****** You crawl out of the dungeon to live and fight another day. ******\n\n")
        return

    if (not enemy.is_alive()):
        print("------")
        print("\t" + enemy.name + " has been defeated!");
        print("\tYou find " + str(enemy.gold) + " gold on the " + enemy.name + "!");
        print("------")


def run_game():
    global enemies, shop_items, potion_types

    player = Character("The player", 100, 30, 20, [])
    player.gold = 1000
    enemies = init_enemies()
    shop_items = init_shop()
    player.inventory.append(potion_types[0])

    must_quit = False
    while player.is_alive() and not must_quit:
        idle_choice = get_idle_choice()
        if (idle_choice == 1):
            fight_common_enemy(player)
        if (idle_choice == 4):
            must_quit = True


if __name__ == "__main__":
    run_game()
