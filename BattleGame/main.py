# Check difference between randint and randrange
# Move "common_enemies" variable so it's not global

import random
from boss import Boss
from character import Character
from player import Player
from item import Item
import utils

bosses = []
common_enemies = []
shop_items = []
potion_types = []


def init_shop():
    global shop_items, potion_types

    shop_items = [
        Item("Silver Sword",  1000, 0, 100, True, 0),
        Item("Steel Sword", 250, 0, 25, True, 0),
        Item("Iron Helmet", 150, 10, 0, True, 0),
        Item("Iron Chestplate", 200, 18, 0, True, 0),
        Item("Iron Boots", 100, 8, 0, True, 0),
        Item("Iron Gauntlets", 75, 5, 0, True, 0),
        Item("Steel Helmet", 400, 5, 0, True, 0),
        Item("Steel Chestplate", 600, 10, 10, True, 0),
        Item("Steel Boots", 300, 10, 0, True, 0),
        Item("Steel Gauntlets", 250, 7, 0, True, 0),
        Item("Illbane", 2500, 0, 0, False, 1),
    ]

    potion_types = [
        Item("Health Potion", 100, 30, 1, False, 0),
        Item("Strength Potion", 500, 0, 2, False, 0)
    ]


def get_shop_choice(player):
    global shop_items, potion_types

    all_items = shop_items + potion_types

    utils.display_status(player)
    print("What would you like to buy?")
    print('{s:{c}^{n}}'.format(s='', n=45, c='#'))
    print("     {:20}| {:>8}|{:>8}|".format("Item", "Health", "Strength"))
    index = 0
    for shopitem in all_items:
        index += 1
        print(" {:2}. {:20}| {:>8}|{:>8}|".format(
            index, shopitem.name, shopitem.health_bonus, shopitem.strength_bonus))
    print(" " + str(index + 1) + ". Exit shop")
    print('{s:{c}^{n}}'.format(s='', n=45, c='#'))

    user_choice = utils.get_valid_input(index + 1)
    if user_choice <= len(all_items):
        return all_items[user_choice - 1]

    return None


def get_potion_choice():
    print("####################")
    index = 0
    for potion in potion_types:
        index += 1
        print(" " + str(index) + ". " + potion.name)
    print("####################")

    return potion_types[get_valid_input(index) - 1]


def visit_shop(player):
    staying_in_shop = True
    staying_in_potion_shop = True

    while (staying_in_shop):
        chosen_item = get_shop_choice(player)
        if (chosen_item == None):
            staying_in_shop = False
        else:
            if (chosen_item.is_wearable) and (chosen_item in player.inventory):
                print("You already have " + chosen_item.name + "!")
                continue

            if (chosen_item.is_wearable):
                if (player.gold >= chosen_item.cost):
                    player.gold -= chosen_item.cost
                    player.illbane += chosen_item.illbane
                    player.base_strength += chosen_item.strength_bonus
                    player.base_health += chosen_item.health_bonus / 2
                    player.inventory.append(chosen_item)
                else:
                    print("You don't have enough gold!")
            else:
                print('How many ' + chosen_item.name + '?')
                amount = utils.get_valid_input(10)
                if (player.gold >= amount * chosen_item.cost):
                    staying_in_shop = False
                    print("You got " + chosen_item.name + "!")
                    player.gold -= amount * chosen_item.cost
                    for i in range(amount):
                        player.inventory.append(chosen_item)
                else:
                    print("You don't have enough gold!")
    print("Goodbye")


def start_battle(player, enemy=None):
    global common_enemies, potion_types

    if (enemy == None):
        enemy = common_enemies[random.randint(0, len(common_enemies) - 1)]

    print("\t# " + enemy.name + " appears! #\n")

    fighting = True

    while (fighting and enemy.is_alive() and player.is_alive()):
        utils.display_status(player, enemy)
        battle_choice = utils.get_battle_choice(player, enemy)
        if (battle_choice == 1):
            damage_dealt = random.randint(0, player.strength - 1)
            damage_taken = enemy.do_attack()
            enemy.health -= damage_dealt
            player.health -= damage_taken
            print("\t> You strike the " + enemy.name +
                  " for " + str(damage_dealt) + " damage.")
            print("\t> You receive " + str(damage_taken) + " in retaliation!")
        if (battle_choice == 2):
            potion = get_potion_choice()
            if (potion in player.inventory):
                player.drink(potion)
            else:
                print("\tYou don't have any " + potion.name + "!")
        if (battle_choice == 3):
            print("------")
            print("\tYou run away from the " + enemy.name + "!")
            print("------")
            fighting = False

    if (not player.is_alive()):
        print("\n****** You crawl out of the dungeon to live and fight another day. ******\n\n")
        return

    if (not enemy.is_alive()):
        dropped_illbane = random.randint(1, 3)
        player.illbane += dropped_illbane
        print("------")
        print("\t" + enemy.name + " has been defeated!")
        print("\tYou find " + str(enemy.gold) +
              " gold on the " + enemy.name + "!")
        print("\tYou collect " + str(dropped_illbane) +
              " illbane from " + enemy.name + "!")
        player.gold += enemy.gold
        item = enemy.get_dropped_object()
        if item != None:
            print("\t" + enemy.name + " has dropped " + item.name + "!")
            player.inventory.append(item)
        print("------")


def sacrifice_illbane(player):
    global bosses

    if player.illbane >= 4:
        player.illbane -= 4
        start_battle(player, bosses[random.randint(0, len(bosses) - 1)])
    else:
        print("\nYou do not have enough illbane!\n")


def run_game():
    global bosses, common_enemies, shop_items, potion_types

    common_enemies = utils.init_common_enemies()
    bosses = utils.init_bosses()
    init_shop()
    player = Player("The player", 100, 30, 20, 1000, [potion_types[0]])
    player.illbane = 1

    must_quit = False
    while player.is_alive() and not must_quit:
        idle_choice = utils.get_idle_choice(player)
        if (idle_choice == 1):
            start_battle(player)
        if (idle_choice == 2):
            visit_shop(player)
        if (idle_choice == 3):
            sacrifice_illbane(player)
        if (idle_choice == 4):
            must_quit = True


if __name__ == "__main__":
    run_game()
