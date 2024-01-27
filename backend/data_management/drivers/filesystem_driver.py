from pathlib import Path
import json
import os

from backend.data_management.base_driver import BaseDriver
from game.card import Card


class FilesystemDriver(BaseDriver):

    def __init__(self, solved_dir: Path, unsolved_dir: Path):
        self.solved_dir = solved_dir
        self.unsolved_dir = unsolved_dir

    @classmethod
    def get_default_driver(cls) -> BaseDriver:
        base_data_dir = Path("../../data")
        # Acknowledging that this isn't great^
        default_solved_dir = base_data_dir / "solved_cards"
        default_unsolved_dir = base_data_dir / "unsolved_cards"
        return cls(solved_dir=default_solved_dir, unsolved_dir=default_unsolved_dir)

    def save_solved_card(self, card: Card) -> bool:
        card_dir = self.solved_dir / card.name
        if card_dir.exists():
            print(f"Card at {card_dir} already exists! Potentially a duplicate card? Not saving")
            return False
        os.mkdir(card_dir)
        metadata_json = card.generate_metadata_json()
        # Saving inside a directory just for the card in case we'll want to add
        # more files
        with open(card_dir / "metadata.json", mode="w") as metadata_file:
            metadata_file.write(metadata_json)
        return True

    def save_unsolved_card(self, card: Card) -> bool:
        card_path = self.unsolved_dir / (card.creator + card.name)
        if card_path.exists():
            print(f"Card at {card_path} already exists! Potentially a duplicate card? Not saving")
            return False
        card_serialisation = card.serialise()
        with open(card_path, mode="wb") as card_file:
            card_file.write(card_serialisation)
        return True

    @staticmethod
    def _serialisation_file_to_card(card_path: Path) -> Card:
        """
        This function receives a path to a card serialisation file, and returns a card object.
        """
        with open(card_path, mode='rb') as card_file:
            serialisation = card_file.read()
        card = Card.deserialize(serialisation)
        return card

    def _get_all_unsolved_cards(self) -> list[Card]:
        unsolved_card_paths = [Path(card_path) for card_path in os.listdir(self.unsolved_dir)]
        cards = []
        for card_path in unsolved_card_paths:
            if not card_path.exists():
                continue
            card = self._serialisation_file_to_card(card_path)
            cards.append(card)
        return cards

    def get_unsolved_card_by_name(self, name: str = None) -> list[Card]:
        # unsolved cards are kept using only their serialisation.
        if name is None:
            return self._get_all_unsolved_cards()
        card_path = self.unsolved_dir / name
        if not card_path.exists():
            raise FileNotFoundError(f"No such unsolved card {card_path}\n Maybe its been solved already?")
        card = self._serialisation_file_to_card(card_path)
        return [card]

    @staticmethod
    def _json_to_card(metadata_path: Path) -> Card:
        """
        This function receives a path to a card metadata file, and returns a card object
        generated from the given metadata file.
        """
        with open(metadata_path, mode='r') as metadata_file:
            metadata_json = metadata_file.read()
            metadata = json.loads(metadata_json)
        card = Card.load_from_metadata(metadata)
        return card

    def _get_all_solved_cards(self) -> list[Card]:
        """
        This function returns a list of all solved cards.
        """
        solved_card_paths = [Path(card_path) for card_path in os.listdir(self.solved_dir)]
        cards = []
        for card_path in solved_card_paths:
            if not card_path.exists():
                continue
            card = self._json_to_card(card_path / "metadata.json")
            cards.append(card)
        return cards

    def get_solved_card_by_name(self, name: str = None) -> list[Card]:
        if name is None:
            return self._get_all_solved_cards()
        card_path = self.solved_dir / name
        if not card_path.exists():
            raise FileNotFoundError(f"No such solved card {card_path}\n")
        card = self._json_to_card(card_path / "metadata.json")
        return [card]
