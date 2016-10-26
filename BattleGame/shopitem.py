class ShopItem:
    def __init__(self, name, cost, armor_bonus, strength_bonus, illbane):
        self.name = name;
        self.cost = cost;
        self.armor_bonus = armor_bonus;
        self.strength_bonus = strength_bonus;
        self.illbane = illbane;
        self.soldOut = False;
