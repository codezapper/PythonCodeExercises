import random
from boss import Boss
from character import Character
from player import Player
from item import Item


def init_bosses():
    bosses_list = [
        Boss("White Dragon", random.randint(150, 250),
             40, 15, random.randint(0, 10000), []),
        Boss("Blue Dragon", random.randint(160, 230),
             45, 25, random.randint(0, 10000), []),
        Boss("Red Dragon", random.randint(170, 220),
             50, 35, random.randint(0, 10000), []),
        Boss("Black Dragon", random.randint(200, 250),
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
