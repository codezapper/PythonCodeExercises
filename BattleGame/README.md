This is a very simple text game to make practice with Python classes.

General description

The basic idea of the game is to have a character (the "player") move from
battle to battle, with breaks in-between to visit a shop that allows to buy
a single random wearable item and some potions.
It is also possible for the player to trigger a "hard battle" by sacrificing
enough "illbane" to summon a stronger enemy.
The player can obtain "illbane" by eniemes that drop it when defeated, or
save money to buy it in the shop.
The goal of the game is to survive as long as possible to get the highest score.

Functional specifications

- The player starts with 100 HP, 30 strength, 20 as the maximum random damage,
1000 gold and an health potion.
- Initially the player can:
  - Start a fight. This triggers the battle choices menu.
  - Visit the shop. This triggers the shop choices menu. Both items and potions
are available.
  - Sacrifice illbale. This triggers a hard battle. The player needs to have
enough illbane for this to happen.
- During the fight the player can:
  - Attack the enemy. This means that the enemy will also attack the player.
The player attack damage is subtracted from the enemy's health and the enemy's
attack damage is subtracted from the player's health. When either reaches zero,
the fight is over. If the player's health reaches zero, the game is also over.
If the enemy is defeated and the player is still alive, the enemy will drop a
random amount of gold and a single unit of illbane. There is a random chance
that the enemy will also drop an health potion. The score will also be updated
based on the enemy value.
  - Drink a potion. Currently two kinds of potions are supported:
    - Health potion. This restores part of the player's health.
    - Strength potion. This increases the player's attack allowing to do more damage.
  - Run from the battle. This ends the current battle and sends the player back to
  the main actions choice.
