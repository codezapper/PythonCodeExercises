# Check difference between randint and randrange
# Move "common_enemies" variable so it's not global

import random
from character import Character
from player import Player
from item import Item

bosses = []
common_enemies = []
shop_items = []
potion_types = []


def init_bosses():
    bosses_list = [
        Character("White Dragon", random.randint(150, 250),
                  40, 15, random.randint(0, 10000), []),
        Character("Blue Dragon", random.randint(160, 230),
                  45, 25, random.randint(0, 10000), []),
        Character("Red Dragon", random.randint(170, 220),
                  50, 35, random.randint(0, 10000), []),
        Character("Black Dragon", random.randint(200, 250),
                  60, 50, random.randint(0, 10000), [])
    ]

    return bosses_list


def init_common_enemies():
    enemy_list = [
        Character("Kobold", random.randint(50, 150),
                  25, 10, random.randint(0, 1000), []),
        Character("Kobold Warrior", random.randint(70, 220),
                  30, 20, random.randint(0, 1000), []),
        Character("Kobold Archer", random.randint(90, 290),
                  40, 30, random.randint(0, 1000), []),
        Character("Kobold Overseer", random.randint(
            150, 400), 50, 40, random.randint(0, 1000), [])
    ]

    return enemy_list


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


def get_valid_input(max_choice):
    user_choice = raw_input()
    while (user_choice == '') or ((user_choice < 1) and (user_choice > max_choice)):
        print "Invalid choice\n"
        user_choice = raw_input()
    return int(user_choice)


def get_battle_choice(player, enemy):
    print("####################")
    print("What would you like to do?")
    print(" 1. Attack")
    print(" 2. Drink potion")
    print(" 3. Run!")
    print("####################")

    return get_valid_input(3)


def get_idle_choice(player):
    display_status(player)
    print(" 1. Fight")
    print(" 2. Visit the shop")
    print(" 3. Sacrifice Illbane...")
    print(" 4. Exit dungeon")
    print("####################")

    return get_valid_input(4)


def get_potion_choice():
    print("####################")
    index = 0
    for potion in potion_types:
        index += 1
        print(" " + str(index) + ". " + potion.name)
    print("####################")

    return potion_types[get_valid_input(index) - 1]


def get_shop_choice(player):
    global shop_items, potion_types

    all_items = shop_items + potion_types

    display_status(player)
    print("What would you like to buy?")
    print("\t  . {:20}| {:>8}|{:>8}|".format("Item", "Health", "Strength"))
    index = 0
    for shopitem in all_items:
        index += 1
        print("\t{:2}. {:20}| {:>8}|{:>8}|".format(
            index, shopitem.name, shopitem.health_bonus, shopitem.strength_bonus))
    print("\t" + str(index + 1) + ". Exit shop")
    print("####################")

    user_choice = get_valid_input(index + 1)
    if user_choice <= len(all_items):
        return all_items[user_choice - 1]

    return None


def display_status(player, enemy=None):
    if (enemy == None):
        print('{s:{c}^{n}}'.format(s='', n=20, c='#'))
        print('# {:>10}'.format('Health: ') +
              '{:6} #'.format(str(player.health)))
        print('# {:>10}'.format('Strength: ') +
              '{:6} #'.format(str(player.strength)))
        print('# {:>10}'.format('Illbane: ') +
              '{:6} #'.format(str(player.illbane)))
        print('# {:>10}'.format('Gold: ') +
              '{:6} #'.format(str(player.gold)))
        print('{s:{c}^{n}}'.format(s='', n=20, c='#'))
    else:
        print('{s:{c}^{n}}'.format(s='', n=40, c='#'))
        print('# {:>10}'.format('Health: ') +
              '{:6} #'.format(str(player.health)) + '# {:>10}'.format('Health: ') +
              '{:6} #'.format(str(enemy.health)))
        print('# {:>10}'.format('Strength: ') +
              '{:6} #'.format(str(player.strength)) + '# {:>10}'.format('Strength: ') +
              '{:6} #'.format(str(enemy.strength)))
        print('# {:>10}'.format('Illbane: ') +
              '{:6} #'.format(str(player.illbane)) + '# {:>10}'.format('Illbane: ') +
              '{:6} #'.format(str(enemy.illbane)))
        print('# {:>10}'.format('Gold: ') +
              '{:6} #'.format(str(player.gold)) + '# {:>10}'.format('Gold: ') +
              '{:6} #'.format(str(enemy.gold)))
        print('{s:{c}^{n}}'.format(s='', n=40, c='#'))


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

            if (player.gold >= chosen_item.cost):
                player.gold -= chosen_item.cost
                player.inventory.append(chosen_item)
                player.illbane += chosen_item.illbane
                if (chosen_item.is_wearable):
                    player.base_strength += chosen_item.strength_bonus
                    player.base_health += chosen_item.health_bonus / 2
                staying_in_shop = False
                print("You got " + chosen_item.name + "!")
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
        display_status(player, enemy)
        battle_choice = get_battle_choice(player, enemy)
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
              " from " + enemy.name + "!")
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

    common_enemies = init_common_enemies()
    bosses = init_bosses()
    init_shop()
    player = Player("The player", 100, 30, 20, 1000, [potion_types[0]])
    player.illbane = 10

    must_quit = False
    while player.is_alive() and not must_quit:
        idle_choice = get_idle_choice(player)
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
