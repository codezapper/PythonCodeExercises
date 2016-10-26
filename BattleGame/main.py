## Check difference between randint and randrange
## Move "enemies" variable so it's not global

import random
from character import Character
from player import Player
from shopitem import ShopItem
from potion import Potion

enemies = []
shop_items = []
potion_types = []

def init_enemies():
    enemy_list = [
        Character("Kobold", random.randint(50, 150), 25, 10, random.randint(0, 1000), []),
        Character("Kobold Warrior", random.randint(70, 220), 30, 20, random.randint(0, 1000), []),
        Character("Kobold Archer", random.randint(90, 290), 40, 30, random.randint(0, 1000), []),
        Character("Kobold Overseer", random.randint(150, 400), 50, 40, random.randint(0, 1000), [])
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

    return int(user_choice)

def get_battle_choice(player, enemy):
    print("------");
    print("\tYour HP is: " + str(player.health))
    print("\tYour strength is: " + str(player.strength))
    print("\t" + enemy.name + "'s HP: " + str(enemy.health))
    print("\n\tWhat would you like to do?")
    print("\t1. Attack")
    print("\t2. Drink potion")
    print("\t3. Run!")
    print("------")

    return get_valid_input(3)

def get_idle_choice():
    print("------------------------------")
    print("\t1. Fight")
    print("\t2. Visit the shop")
    print("\t3. Sacrifice Illbane...")
    print("\t4. Exit dungeon")
    print("------------------------------")

    return get_valid_input(4)

def get_potion_choice():
    index = 0

    print("------------------------------")
    for potion in potion_types:
        index += 1
        print("\t" + str(index) + ". " + potion.name)
    print("------------------------------")

    return potion_types[get_valid_input(index)-1]


def get_shop_choice():
    print("------------------------------")
    print("What would you like to buy?")
    for shopitem in shop_items:
        index += 1
        print("\t" + str(index) + ". " + shopitem.name)

    print("------------------------------")

    return shop_items[get_valid_input(index)-1]

def visit_shop(player):
    if (get_shop_choice() == len(shop_items)):
        print("Goodbye")
    else:

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
            potion = get_potion_choice()
            if (potion in player.inventory):
                player.drink(potion)
            else:
                print("\tYou don't have any " + potion.name + "!")
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
        player.gold += enemy.gold
        print("------")


def run_game():
    global enemies, shop_items, potion_types

    enemies = init_enemies()
    shop_items = init_shop()
    player = Player("The player", 100, 30, 20, [potion_types[0]])
    player.gold = 1000

    must_quit = False
    while player.is_alive() and not must_quit:
        idle_choice = get_idle_choice()
        if (idle_choice == 1):
            fight_common_enemy(player)
        if (idle_choice == 2):
            visit_shop(player)
        if (idle_choice == 4):
            must_quit = True


if __name__ == "__main__":
    run_game()
