class ShopItem:
    def __init__(self, name, cost, armor_bonus, attack_bonus, illbane):
        self.name = name;
        self.cost = cost;
        self.armor_bonus = armor_bonus;
        self.attack_bonus = attack_bonus;
        self.illbane = illbane;
        self.soldOut = False;
