from pathlib import Path
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
    def save(card: Card, dir_path: Path = None):
        """
        This function receives a card and a path to which to store it, and stores the card under a new directory in
        the given directory.
        Thread sensitive! Use locks.

        :param card: The card object to be saved
        :param dir_path: The directory in which to store the card serialisation
        """
        if dir_path is None:
            dir_path = Path('../../game')
        card_path = dir_path / card.name
        os.mkdir(card_path)
        card_data = card.serialise()

        with open(card_path, mode="wb") as card_file:
            card_file.write(card_data)

    @staticmethod
    def get_free_id(unsolved_path: Path = None) -> int:
        i = 0
        if unsolved_path is None:
            unsolved_path = Path('../../game')
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
            dir_path = Path('../data')
        card_path = dir_path / str(Saver.get_free_id(dir_path))
        with open(card_path, mode="wb") as card_file:
            card_file.write(card)


