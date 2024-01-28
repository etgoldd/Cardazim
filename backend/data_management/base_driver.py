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
    def get_unsolved_card_by_name(self, name: str = None) -> list[Card]:
        """
        This function receives a name and returns the card with the given name.
        :param name: The name of the card to be returned.
        :return: A list of cards, either a singleton, or all of the unsolved cards (if no name is given).
        """
        pass

    @abstractmethod
    def get_solved_card_by_name(self, name: str = None) -> list[Card]:
        """
        This function receives a name and returns the card with the given name.
        :param name: The name of the card to be returned.
        :return: A list of cards, either a singleton, or all of the solved cards (if no name is given).
        """
        pass

    @abstractmethod
    def get_unsolved_cards_by_creator(self, creator: str) -> list[Card]:
        """
        This function receives a creator and returns all the cards of the given creator.
        :param creator: The creator of the cards to be returned.
        :return: A list of all the cards of the given creator.
        """
        pass

    @abstractmethod
    def get_solved_cards_by_creator(self, creator: str) -> list[Card]:
        """
        This function receives a creator and returns all the cards of the given creator.
        :param creator: The creator of the cards to be returned.
        :return: A list of all the cards of the given creator.
        """
        pass

    @abstractmethod
    def get_solved_cards(self, name: str = None, creator: str = None) -> list[Card]:
        """
        This function receives a name and a creator and returns all the cards of the given creator.
        if creator is None, returns all solved cards, if name is None, returns all cards of the given creator.
        :param name: The name of the card to be returned.
        :param creator: The creator of the cards to be returned.
        :return: A list of all the cards of the given creator.
        """
        pass