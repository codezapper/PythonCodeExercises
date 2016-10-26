import random

## Randomize gold if not specified

class Character:
    def __init__(self, name, initial_health, initial_strength, max_random_damage, gold, inventory):
        self.name = name
        self.initial_health = initial_health
        self.health = initial_health
        self.initial_strength = initial_strength
        self.strength = initial_strength
        self.inventory = inventory
        self.max_random_damage = max_random_damage
        self.gold = gold

    def is_alive(self):
        if self.health > 1:
            return True
        return False

    def base_attack(self):
        return self.strength + random.randint(0, self.max_random_damage)
