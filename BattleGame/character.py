import random

## Randomize gold if not specified

class Character:
    def __init__(self, name, base_health, base_strength, max_random_damage, gold, inventory):
        self.name = name
        self.base_health = base_health
        self.health = base_health
        self.base_strength = base_strength
        self.strength = base_strength
        self.inventory = inventory
        self.max_random_damage = max_random_damage
        self.gold = gold
        self.armor = 0

    def is_alive(self):
        if self.health > 1:
            return True
        return False

    def base_attack(self):
        return self.strength + random.randint(0, self.max_random_damage)
