from __future__ import annotations

from pymongo import MongoClient
from typing import Mapping, Any

from backend.data_management.base_driver import BaseDriver
from exceptions import CardNotFound
from game.card import Card

DEFAULT_MONGO_CONN_STR = "mongodb://127.0.0.1:27017"
DEFAULT_DATABASE_NAME = "CARDAZIM"
DEFAULT_UNSOLVED_COLLECTION_NAME = "unsolved_cards"
DEFAULT_SOLVED_COLLECTION_NAME = "solved_cards"


class MongoDriver(BaseDriver):

    def __init__(self,
                 mongo_conn_str: str,
                 database_name: str,
                 unsolved_cards_collection_name: str,
                 solved_cards_collection_name: str):
        self.client = MongoClient(mongo_conn_str)
        self.database = self.client.get_database(database_name)
        self.solved_cards_collection = self.database.get_collection(solved_cards_collection_name)
        self.unsolved_cards_collection = self.database.get_collection(unsolved_cards_collection_name)

    @classmethod
    def get_default_driver(cls) -> MongoDriver:
        return cls(DEFAULT_MONGO_CONN_STR,
                   DEFAULT_DATABASE_NAME,
                   DEFAULT_UNSOLVED_COLLECTION_NAME,
                   DEFAULT_SOLVED_COLLECTION_NAME)

    def save_solved_card(self, card: Card) -> bool:
        card_dict = {'name': card.name,
                     'creator': card.creator,
                     'riddle': card.riddle,
                     'image_path': card.image_path,
                     'solution': card.solution}
        if None in card_dict.values():
            print("Card is missing fields, not saving...")
            return False
        self.solved_cards_collection.insert_one(card_dict)
        return True

    def save_unsolved_card(self, card: Card) -> bool:
        card_dict = {'name': card.name,
                     'creator': card.creator,
                     'riddle': card.riddle,
                     'image_path': card.image_path,
                     'key_hash': card.image.key_hash}
        if None in card_dict.values():
            print("Card is missing fields, not saving...")
            return False
        self.unsolved_cards_collection.insert_one(card_dict)
        return True

    @staticmethod
    def _document_to_card(card_document: Mapping[str, Any], solved: bool) -> Card:
        """
        This function receives a card document and returns a card object from the fields
        in the document.
        :param card_document: The document to be converted to a card.
        :param solved: Whether the card is solved or not, affects the filled fields (key_hash vs solution).
        :return:
        """
        name = card_document.get('name')
        creator = card_document.get('creator')
        riddle = card_document.get('riddle')
        path = card_document.get('image_path')
        solution = None
        key_hash = None
        if solved:
            solution = card_document.get('solution')
        else:
            key_hash = card_document.get('key_hash')
        card = Card.create_from_path(name, creator, path, riddle, solution, key_hash)
        return card

    def _get_all_solved_cards(self) -> list[Card]:
        """
        This function returns a list of all solved cards.
        """
        card_documents = self.solved_cards_collection.find()
        cards = []
        for card_document in card_documents:
            card = self._document_to_card(card_document, solved=True)
            cards.append(card)
        return cards

    def get_solved_card_by_name(self, name: str = None) -> list[Card]:
        if name is None:
            return self._get_all_solved_cards()
        card_document = self.solved_cards_collection.find_one({'name': name})
        if card_document is None:
            raise CardNotFound(f"No such card with name: '{name}'.")
        card = self._document_to_card(card_document, solved=True)
        return [card]

    def _get_all_unsolved_cards(self) -> list[Card]:
        """
        This function returns a list of all unsolved cards.
        """
        card_documents = self.unsolved_cards_collection.find()
        cards = []
        for card_document in card_documents:
            card = self._document_to_card(card_document, solved=False)
            cards.append(card)
        return cards

    def get_unsolved_card_by_name(self, name: str = None, creator: str = None) -> list[Card]:
        if name is None or creator is None:
            return self._get_all_unsolved_cards()
        card_document = self.unsolved_cards_collection.find_one({'name': name, 'creator': creator})
        if card_document is None:
            raise CardNotFound(f"No such card with name: '{name}'.")
        card = self._document_to_card(card_document, solved=False)
        return [card]

    def get_unsolved_cards_by_creator(self, creator: str) -> list[Card]:
        card_documents = self.unsolved_cards_collection.find({'creator': creator})
        cards = []
        for card_document in card_documents:
            card = self._document_to_card(card_document, solved=False)
            cards.append(card)
        return cards

    def get_solved_cards_by_creator(self, creator: str) -> list[Card]:
        card_documents = self.solved_cards_collection.find({'creator': creator})
        cards = []
        for card_document in card_documents:
            card = self._document_to_card(card_document, solved=True)
            cards.append(card)
        return cards

    def get_solved_cards(self, name: str = None, creator: str = None) -> list[Card]:
        if name is None:
            return self.get_solved_cards_by_creator(creator)
        if creator is None:
            return self._get_all_solved_cards()
        card_documents = self.solved_cards_collection.find({'name': name, 'creator': creator})
        cards = []
        for card_document in card_documents:
            card = self._document_to_card(card_document, solved=True)
            cards.append(card)
        return cards
