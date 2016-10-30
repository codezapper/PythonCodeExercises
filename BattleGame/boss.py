from character import Character
import random

# Randomize gold if not specified


class Boss(Character):
    special_attack_chance = 0

    def do_special_attack(self):
        print(self.name + " launches its special attack!")
        return random.randint(self.strength, self.strength + self.max_random_damage)

    def do_attack(self):
        self.special_attack_chance += (self.health / self.base_health) * 100
        chance = random.randint(0, 100)
        print(chance, self.special_attack_chance)
        if (chance < self.special_attack_chance):
            return self.do_special_attack()
        else:
            return random.randint(0, self.max_random_damage)
