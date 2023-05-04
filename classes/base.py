from classes.unit import BaseUnit
from typing import Optional


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND: float = 1
    player: BaseUnit = None
    enemy: BaseUnit = None
    game_is_running: bool = False
    game_result: str = ""

    def start_game(self, player: BaseUnit, enemy: BaseUnit) -> None:
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self) -> Optional[str]:
        if self.player.hp <= 0:
            self.game_result = "Удача оказалась не на твоей стороне, ты проиграл.\nПопробуй ещё раз."
            return self._end_game()
        elif self.enemy.hp <= 0:
            self.game_result = "Противник повержен, ты победил!"
            return self._end_game()
        elif self.player.hp <= 0 and self.enemy.hp <= 0:
            self.game_result = "Оба бойца пали, ничья"
            return self._end_game()

    def _stamina_regeneration(self) -> None:
        self.player.regenerate_stamina(self.STAMINA_PER_ROUND)
        self.enemy.regenerate_stamina(self.STAMINA_PER_ROUND)

    def next_turn(self) -> str:
        result = self._check_players_hp()
        if result:
            return result
        self._stamina_regeneration()
        result = self.enemy.hit(self.player)
        return result

    def _end_game(self) -> str:
        self.game_is_running = False
        return self.game_result

    def player_hit(self) -> str:
        result = self.player.hit(self.enemy)
        self.next_turn()
        return result

    def player_use_skill(self) -> str:
        result = self.player.use_skill(self.enemy)
        self.next_turn()
        return result
