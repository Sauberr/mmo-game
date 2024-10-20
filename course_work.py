from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Union
import random
from time import sleep
from colorama import Fore, Style


class CustomException(BaseException):
    pass


class Character(ABC):
    __slots__ = ('name', 'health', 'strength', 'speed', 'mana', 'weapon', 'armor',)

    def __init__(self, name: str = 'Alex', health: int = 100, strength: int = 1, speed: int = 1,
                 mana: int = None, weapon: str = None, armor: int = None) -> None:
        self.name = name
        self.health = health
        self.strength = strength
        self.speed = speed
        self.mana = mana
        self.weapon = weapon
        self.armor = armor

    @abstractmethod
    def _passive_ability(self) -> None:
        pass

    @abstractmethod
    def attack(self, enemy: Union['Character']) -> None:
        pass

    @abstractmethod
    def move(self, enemy: Union['Character']) -> None:
        pass

    def __str__(self) -> str:
        return (f"Name: {self.name}, Health: {self.health}, Strength: {self.strength}, Speed: {self.speed}, Mana: "
                f"{self.mana}, Weapon: {self.weapon}, Armor: {self.armor}")


class Juggernaut(Character):
    def __init__(self, name: str = 'Octain', health: int = 225, strength: int = 5, speed: int = 2, mana: int = None,
                 weapon: str = 'axe', armor: int = 3) -> None:
        super().__init__(name, health, strength, speed, mana, weapon, armor)

    def _passive_ability(self) -> None:
        if self.health < self.health / 2:
            self.strength += 2
            print(Fore.GREEN + Style.BRIGHT + f'{self.name} passive ability activated and now his strength '
                                              f'is {self.strength}')

    def attack(self, enemy: Union['Sentinel', 'Valkyrie', 'Vampire']) -> None:
        self._passive_ability()
        crit_hit = random.randint(1, 5)
        if crit_hit == 5:
            enemy.health -= 200
            print(Fore.GREEN + Style.BRIGHT + f"{self.name} attacked {enemy.name} with {self.weapon} and dealt 200 "
                                              f"crit damage and now {enemy.name} has {enemy.health} health")
        else:
            enemy.health -= 100
            print(Fore.RED + Style.BRIGHT + f"{self.name} attacked {enemy.name} with {self.weapon} and dealt "
                                            f"100 damage and now {enemy.name} has {enemy.health} health")

    def move(self, enemy: Union['Sentinel', 'Valkyrie']) -> None:
        self._passive_ability()
        if enemy.speed <= self.speed:
            print(Fore.WHITE + Style.BRIGHT + f'Character {self.name} have more speed than {enemy.name} and '
                                              f'can attack first')

    def heal(self) -> None:
        self._passive_ability()
        if self.health < 350:
            heal = random.randint(1, 5)
            if heal == 5:
                self.health += 25
                print(Fore.GREEN + Style.BRIGHT + f'{self.name} healed himself and now has {self.health} health')
            else:
                print(Fore.RED + Style.BRIGHT + f'{self.name} tried to heal himself but failed')

    def __str__(self) -> str:
        return super().__str__()


class Sentinel(Character):
    def __init__(self, name: str = 'Newcastle', health: int = 400, strength: int = 2, speed: int = 1,
                 mana: int = None, weapon: str = 'shield', armor: int = 10) -> None:
        super().__init__(name, health, strength, speed, mana, weapon, armor)

    def _passive_ability(self, enemy: Union['Vampire', 'Valkyrie', 'Juggernaut']) -> None:
        enemy.strength -= Decimal(1 - 0.25)
        print(Fore.GREEN + Style.BRIGHT + f'{self.name} passive ability activated and now {enemy.name} attack is '
                                          f'{enemy.strength} damage.')

    def attack(self, enemy: Union['Juggernaut', 'Vampire', 'Valkyrie']) -> None:
        self._passive_ability(enemy)
        enemy.health -= 100
        print(Fore.WHITE + Style.BRIGHT + f"{self.name} attacked {enemy.name} with {self.weapon} and dealt 100 damage "
                                          f"and now {enemy.name} has {enemy.health} health.")

    def move(self, enemy: Union['Juggernaut', 'Valkyrie']) -> None:
        self._passive_ability(enemy)
        if enemy.speed <= self.speed:
            print(f'Character {self.name} have more speed than {enemy.name} and can attack first.')

    def block(self, enemy: Union['Juggernaut', 'Vampire', 'Valkyrie']) -> None:
        enemy.attack = 0
        print(Fore.WHITE + Style.BRIGHT + f' {self.name} blocked {enemy.name} attack and now {enemy.name} attack is'
                                          f' {enemy.attack} damage.')

    def __str__(self) -> str:
        return super().__str__()


class Valkyrie(Character):
    def __init__(self, name: str = 'Janna', health: int = 250, strength: int = 4, speed: int = 3,
                 mana: int = 150, weapon: str = 'spear', armor: int = 3) -> None:
        super().__init__(name, health, strength, speed, mana, weapon, armor)

    def _passive_ability(self) -> None:
        self.mana += 10
        print(Fore.GREEN + Style.BRIGHT + f'{self.name} passive ability activated and now has {self.mana} mana.')

    def attack(self, enemy: Union['Sentinel', 'Juggernaut', 'Vampire']) -> None:
        self._passive_ability()
        crit_hit = random.randint(1, 5)
        if crit_hit == 5:
            enemy.health -= 200
            print(Fore.GREEN + Style.BRIGHT + f"{self.name}: ({type(self).__name__}) attacked {enemy.name}: "
                                              f"({type(self).__name__}) with {self.weapon} and dealt 200 crit damage and"
                                              f" now {enemy.name}: ({type(self).__name__}) has {enemy.health} health.")
        else:
            print('Crit attack failed')
            enemy.health -= 100
            print(Fore.RED + Style.BRIGHT + f"{self.name}: ({type(self).__name__}) attacked {enemy.name} with "
                                            f"{self.weapon} and dealt 100 damage and now {enemy.name}: "
                                            f"({type(self).__name__}) has {enemy.health} health.")

    def move(self, enemy: Union['Sentinel', 'Juggernaut']) -> None:
        self._passive_ability()
        if enemy.speed <= self.speed:
            print(Fore.WHITE + Style.BRIGHT + f'Character {self.name}: ({type(self).__name__}) have more speed than '
                                              f'{enemy.name}: ({type(self).__name__}) and can attack first.')

    def fly(self,  enemy: Union['Sentinel', 'Juggernaut', 'Vampire']) -> None:
        self._passive_ability()
        original_strength = enemy.strength
        if self.mana > 70:
            self.mana -= 70
            enemy.health -= 150
            enemy.attack = 0
            enemy.strength -= 2
            print(Fore.WHITE + Style.BRIGHT + f'{self.name}: ({type(self).__name__}) used fly ability and '
                                              f'now {enemy.name}: ({type(self).__name__}) health is {enemy.health}, '
                                              f'strength is {enemy.strength} and attack is {enemy.attack}.')
            sleep(7)
            enemy.strength = original_strength
            print(Fore.WHITE + Style.BRIGHT + f'{self.name}: ({type(self).__name__}) used fly ability and '
                                              f'now {enemy.name}: ({type(self).__name__}) health is {enemy.health},'
                                              f' strength is {enemy.strength} after 7 sec strength will be '
                                              f'{original_strength} and attack is {enemy.attack}.')

    def __str__(self) -> str:
        return super().__str__()


class Vampire(Character):
    def __init__(self, name: str = 'Dracula', health: int = 175, strength: int = 4, speed: int = 3,
                 mana=None, weapon: str = 'fangs', armor: int = 2) -> None:
        super().__init__(name, health, strength, speed, mana, weapon, armor)

    def _passive_ability(self) -> None:
        self.health += 10
        print(Fore.GREEN + Style.BRIGHT + f'{self.name}: ({type(self).__name__}) passive ability activated and now '
                                          f'has {self.health} health')

    def attack(self, enemy: Union['Juggernaut', 'Valkyrie', 'Sentinel']) -> None:
        self._passive_ability()
        crit_hit = random.randint(1, 5)
        if crit_hit == 5:
            enemy.health -= 200
            self.health -= 5
            print(Fore.GREEN + Style.BRIGHT + f"{self.name}: ({type(self).__name__}) attacked {enemy.name} with "
                                              f"{self.weapon} and dealt 200 crit damage and now {enemy.name} has "
                                              f"{enemy.health} health and {self.name}: ({type(self).__name__}) has "
                                              f"{self.health} health.")
        else:
            enemy.health -= 125
            self.health -= 2
            print(Fore.RED + Style.BRIGHT + f"{self.name}: ({type(self).__name__}) attacked {enemy.name} with "
                                            f"{self.weapon} and dealt 125 damage and now {enemy.name} has {enemy.health} "
                                            f"health and {self.name}: ({type(self).__name__}) has {self.health} health.")

    def move(self, enemy: Union['Sentinel', 'Juggernaut', 'Valkyrie']) -> None:
        self._passive_ability()
        if enemy.speed <= self.speed:
            print(Fore.WHITE + Style.BRIGHT + f'Character {self.name}: ({type(self).__name__}) have more speed '
                                              f'than {enemy.name}: ({type(self).__name__} and can attack first.')

    def bite(self, enemy: Union['Sentinel', 'Juggernaut', 'Valkyrie']) -> None:
        self._passive_ability()
        original_strength = enemy.strength
        if self.health > 15:
            self.health -= 15
            enemy.health -= 50
            enemy.strength -= 1
            sleep(10)
            print(Fore.GREEN + Style.BRIGHT + f'{self.name}: ({type(self).__name__}) used bite ability and now '
                                              f'{enemy.name}: ({type(self).__name__}) health is {enemy.health} '
                                              f'and strength is {enemy.strength}.')
            enemy.strength = original_strength
            print(Fore.RED + Style.BRIGHT + f'{self.name}: ({type(self).__name__}) used bite ability and now '
                                            f'{enemy.name}: ({type(self).__name__}) health is {enemy.health} and '
                                            f'strength is {enemy.strength} after 10 sec strength will be {original_strength}.')

    def __str__(self) -> str:
        return super().__str__()


class Game:
    def start(self):
        username = str(input('Enter your hero name: '))
        print('Game started')
        print('Choose your hero: \n' + \
              '1. Juggernaut \n' + \
              '2. Sentinel \n' + \
              '3. Valkyrie \n' + \
              '4. Vampire \n' + \
              '5. Exit'
              )

        try:
            choice_hero = int(input('Enter your choice: '))

            if choice_hero == 1:
                juggernaut = Juggernaut(username)
                sentinel = Sentinel()
                valkyrie = Valkyrie()
                vampire = Vampire()
            elif choice_hero == 2:
                sentinel = Sentinel(username)
                juggernaut = Juggernaut()
                valkyrie = Valkyrie()
                vampire = Vampire()
            elif choice_hero == 3:
                valkyrie = Valkyrie(username)
                juggernaut = Juggernaut()
                sentinel = Sentinel()
                vampire = Vampire()
            elif choice_hero == 4:
                vampire = Vampire(username)
                juggernaut = Juggernaut()
                sentinel = Sentinel()
                valkyrie = Valkyrie()
            elif choice_hero == 5:
                self.end()
            else:
                raise CustomException(Fore.RED + Style.BRIGHT + 'Error: Invalid choice')

            juggernaut.attack(sentinel)
            sentinel.attack(juggernaut)
            valkyrie.attack(vampire)
            vampire.attack(valkyrie)

            juggernaut.move(sentinel)
            sentinel.move(juggernaut)
            valkyrie.move(vampire)
            vampire.move(valkyrie)

            juggernaut.heal()
            sentinel.block(juggernaut)
            valkyrie.fly(sentinel)
            vampire.bite(valkyrie)

        except CustomException as e:
            print(e)

    def end(self):
        return 'Game ended'


if __name__ == '__main__':
    start_game = Game()
    start_game.start()
