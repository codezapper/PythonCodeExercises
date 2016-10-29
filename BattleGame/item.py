class Item:

    def __init__(self, name, cost, health_bonus, strength_bonus, wearable, illbane):
        self.name = name
        self.cost = cost
        self.health_bonus = health_bonus
        self.strength_bonus = strength_bonus
        self.illbane = illbane
        self.soldOut = False
        self.is_wearable = wearable
