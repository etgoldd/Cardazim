from pathlib import Path
import json
import os


from game.card import Card


class Saver:

    @staticmethod
    def extract_card(path: Path) -> Card:
        with open(path, mode="rb") as card_file:
            card_serialisation = b""
            while section := card_file.read() != b"":
                card_serialisation += section
        try:
            return Card.deserialize(card_serialisation)
        except Exception as e:
            print(f"Are you sure you gave the right path? Attempted to deserialize card at {path} and failed. "
                  f"Raising error...\n")
            raise e

    @staticmethod
    def generate_metadata_json(card: Card, dir_path: Path = None) -> bool:
        """
        This function receives a card and a path in which to store the cards metadata.
        Will return True if succeeded, and false otherwise.
        :param card: The card for which to generate the json file.
        :param dir_path: The path in which to store the metadata.json file
        :return: Whether the generation succeeded
        """
        if dir_path is None:
            dir_path = Path('.')
        file_dir = dir_path / "metadata.json"
        try:
            encoder = json.JSONEncoder()
            card_json = encoder.encode(card.get_attributes())
        except TypeError as e:
            print(f"Something has gone wrong while saving the card, here's the card: \n{str(card)} \n raising error...")
            raise e
        except ValueError as e:
            print(f"Something has gone wrong while saving the card, here's the card: \n{str(card)} \n raising error...")
            raise e

        with open(file_dir, mode="w") as metadata_file:
            metadata_file.write(card_json)

        return True


    @staticmethod
    def save(card: Card, dir_path: Path = None):
        """
        This function receives a card and a path to which to store it, and stores the card under a new directory in
        the given directory.
        Thread sensitive! Use locks.

        :param card: The card object to be saved
        :param dir_path: The directory in which to store the card serialisation
        """
        if dir_path is None:
            dir_path = Path('.')
        card_path = dir_path / card.name
        os.mkdir(card_path)
        card_data = card.serialise()

        with open(card_path, mode="wb") as card_file:
            card_file.write(card_data)

    @staticmethod
    def get_free_id(unsolved_path: Path = None) -> int:
        i = 0
        if unsolved_path is None:
            unsolved_path = Path('.')
        while True:
            if not (unsolved_path / str(i)).exists():
                return i
            # If the file exists, we'll try the next one
            i += 1

    @staticmethod
    def save_serialisation(card: bytes, dir_path: Path = None):
        """
        This function receives a card and a path to which to store it, and stores the card under a new directory in
        :param card: The card object to be saved
        :param dir_path: The directory in which to store the card serialisation
        :return:
        """
        if dir_path is None:
            dir_path = Path('.')
        card_path = dir_path / str(Saver.get_free_id(dir_path))
        with open(card_path, mode="wb") as card_file:
            card_file.write(card)


