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
        This function receives an id and returns the card with the given id.
        :param _id: The id of the card to be returned. Check Card class to see what a card's id is.
        :return: A list of cards, either a singleton, or all of the unsolved cards (if no id is given).
        """
        pass

    @abstractmethod
    def get_solved_card_by_name(self, name: str = "") -> list[Card]:
        """
        This function receives a name and returns the card with the given name.
        :param name: The name of the card to be returned.
        :return: A list of cards, either a singleton, or all of the solved cards (if no name is given).
        """
        pass
