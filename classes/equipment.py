from dataclasses import dataclass
from typing import List
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    id: int
    name: str
    defense: float
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        return uniform(self.min_damage, self.max_damage)


@dataclass
class EquipmentData:
    armors: List[Armor]
    weapons: List[Weapon]


class Equipment:

    def __init__(self):
        self.equipment: EquipmentData = self._get_equipment_data()

    def get_weapon(self, weapon_name: str) -> Weapon:
        for weapon in self.equipment.weapons:
            if weapon_name.lower() == weapon.name.lower():
                return weapon

    def get_armor(self, armor_name: str) -> Armor:
        for armor in self.equipment.armors:
            if armor_name.lower() == armor.name.lower():
                return armor

    def get_weapons_names(self) -> list:
        return [weapon.name for weapon in self.equipment.weapons]

    def get_armors_names(self) -> list:
        return [armor.name for armor in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        with open("./data/equipment.json", "r", encoding="utf-8") as equipment_file:
            data = json.load(equipment_file)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
