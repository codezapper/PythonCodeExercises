# Check difference between randint and randrange
# Move "common_enemies" variable so it's not global

import random
from boss import Boss
from character import Character
from player import Player
from item import Item
from shop import Shop
import utils

bosses = []
common_enemies = []
shop_items = []
potion_types = []


def start_battle(player, enemy=None):
    global common_enemies, all_potions

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
            potion = utils.get_potion_choice(all_potions)
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
    global bosses, common_enemies, shop_items, all_potions

    common_enemies = utils.init_common_enemies()
    bosses = utils.init_bosses()
    shop = Shop()
    all_potions = utils.get_all_potions()
    player = Player("The player", 100, 30, 20, 1000,
                    [all_potions[0]])
    player.illbane = 1

    must_quit = False
    while player.is_alive() and not must_quit:
        idle_choice = utils.get_idle_choice(player)
        if (idle_choice == 1):
            start_battle(player)
        if (idle_choice == 2):
            shop.visit(player)
        if (idle_choice == 3):
            sacrifice_illbane(player)
        if (idle_choice == 4):
            must_quit = True


if __name__ == "__main__":
    run_game()
