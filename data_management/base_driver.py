from __future__ import annotations
from abc import abstractmethod


from game.card import Card


class BaseDriver:

    @classmethod
    @abstractmethod
    def get_default_driver(cls) -> BaseDriver:
        pass

    @abstractmethod
    def save_unsolved_card(self, card: Card) -> bool:
        pass

    @abstractmethod
    def save_solved_card(self, card: Card) -> bool:
        pass

    @abstractmethod
    def get_unsolved_card_by_id(self, _id: str = "") -> list[Card]:
        """
        Implementation should make it so when no id is given,
        the method returns all unsolved cards
        """
        pass

    @abstractmethod
    def get_solved_card_by_name(self, name: str = "") -> list[Card]:
        """
        Implementation should make it so when no name is given,
        the method returns all solved cards
        """
        pass
