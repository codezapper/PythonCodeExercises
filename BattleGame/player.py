from character import Character
from potion import Potion
import random


class Player(Character):

    def drink(self, potion):
        self.strength *= potion.strength_bonus
        self.health += potion.health_bonus
        if (self.health > self.base_health):
            self.health = self.base_health
        self.inventory.remove(potion)
        print("You drink a " + potion.name + "!")
