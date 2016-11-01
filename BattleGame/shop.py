import utils
from item import Item


class Shop:

    def __init__(self):
        self.items = [
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

        self.potions = utils.get_all_potions()

    def get_item_choice(self, player):
        all_items = self.items + self.potions

        utils.display_status(player)
        print('What would you like to buy?')
        print('{s:{c}^{n}}'.format(s='', n=54, c='#'))
        print("     {:20}| {:>8}|{:>8}|{:>8}|".format(
            'Item', 'Health', 'Strength', 'Cost'))
        index = 0
        for shopitem in all_items:
            index += 1
            print(' {:2}. {:20}| {:>8}|{:>8}|{:>8}|'.format(
                index, shopitem.name, shopitem.health_bonus, shopitem.strength_bonus, shopitem.cost))
        print(' ' + str(index + 1) + '. Exit shop')
        print('{s:{c}^{n}}'.format(s='', n=54, c='#'))

        user_choice = utils.get_valid_input(index + 1)
        if user_choice <= len(all_items):
            return all_items[user_choice - 1]

        return None

    def visit(self, player):
        staying_in_shop = True
        staying_in_potion_shop = True

        while (staying_in_shop):
            chosen_item = self.get_item_choice(player)
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
