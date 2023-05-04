from __future__ import annotations

from abc import ABC, abstractmethod
from classes.equipment import Equipment, Weapon, Armor
from classes.classes import UnitClass
from random import uniform, randint


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp: float = unit_class.max_health
        self.stamina: float = unit_class.max_stamina
        self.weapon: Weapon = Equipment().get_weapon(weapon_name='топорик')
        self.armor: Armor = Equipment().get_armor(armor_name='кожаная броня')
        self.is_skill_used: bool = False
        self.text_list = [
            [", используя", ", пробивает ", " соперника и наносит ", " урона."],
            [", используя", ", наносит удар, но ", " cоперника его останавливает"],
            [" попытался использовать ", ", но у него не хватило выносливости."]
        ]

    @property
    def health_points(self):
        return round(self.hp, 1)

    @property
    def stamina_points(self):
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> float:
        # УРОН = УРОН_АТАКУЮЩЕГО - БРОНЯ_ЦЕЛИ
        # урон_от_оружия = случайное число в диапазоне (min_damage - max_damage)
        # УРОН_АТАКУЮЩЕГО = урон_от_оружия * модификатор_атаки_класса
        # БРОНЯ_ЦЕЛИ = надетая_броня * модификатор_брони_класса

        weapon_damage = uniform(self.weapon.min_damage, self.weapon.max_damage)
        attacker_damage = weapon_damage * self.unit_class.attack
        target_armor = 0

        if target.stamina >= target.armor.stamina_per_turn:
            target_armor = self.unit_class.armor * target.armor.defense
            target._count_stamina(target.armor.stamina_per_turn)

        if target_armor >= attacker_damage:
            return 0

        damage = round(attacker_damage - target_armor, 1)
        self._count_stamina(self.weapon.stamina_per_hit)

        return damage

    def _count_stamina(self, stamina: float) -> None:
        self.stamina = round(self.stamina - stamina, 1)

    def regenerate_stamina(self, stamina_point: float) -> None:
        stamina_growth: float = stamina_point * self.unit_class.stamina
        if self.stamina + stamina_growth > self.unit_class.max_stamina:
            self.stamina = self.unit_class.max_stamina
        else:
            self.stamina += stamina_growth

    def get_damage(self, damage: float) -> None:
        self.hp = round(self.hp - damage, 1)

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        Этот метод не будет переопределен ниже
        """
        text_1 = self.text_list[0]
        text_2 = self.text_list[1]
        text_3 = self.text_list[2]

        if self.stamina >= self.weapon.stamina_per_hit:
            damage = self._count_damage(target)
            damage = round(damage, 1)

            if damage > 0:
                return f"{self.name}{text_1[0]}{self.weapon.name}{text_1[1]}" \
                       f" {target.armor.name}{text_1[2]}{damage}{text_1[2]}"
            else:
                return f"{self.name}{text_2[0]}{self.weapon.name}{text_2[0]}{target.armor.name}{text_2[2]}"
        else:
            return f"{self.name}{text_3[0]}{self.weapon.name}{text_3[1]}"

    def use_skill(self, target: BaseUnit) -> str:
        """
        Метод использования умения.
        Если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку, которая характеризует выполнение умения
        """
        if self.is_skill_used:
            return "Навык уже использован"
        self.is_skill_used = True
        return self.unit_class.skill.use(user=self, target=target)


class PlayerUnit(BaseUnit):
    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        Вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """
        self.text_list = [
            [", используя", ", пробивает ", " соперника и наносит ", " урона."],
            [", используя", ", наносит удар, но ", " cоперника его останавливает"],
            [" попытался использовать ", ", но у него не хватило выносливости."]
        ]

        return super().hit(target)


class EnemyUnit(BaseUnit):
    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение применено, противник наносит простой удар, где также используется
        функция _count_damage(target)
        """
        if randint(1, 10) == 1 and not self.is_skill_used:
            return self.use_skill(target)

        self.text_list = [
            [", используя", ", пробивает ", " и наносит тебе ", " урона. "],
            [", используя", ", наносит удар, но твоя", "его останавливает."],
            [" попытался использовать ", ", но у него не хватило выносливости."]
        ]

        return super().hit(target)
