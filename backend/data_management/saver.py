from pathlib import Path

from game.card import Card
from backend.data_management.driver_manager import DriverManager

CREATORS_FILE = Path('backend/data/creators.txt')


class Saver:
    def __init__(self):
        self.driver = DriverManager("MONGO").get_default_driver()

    @staticmethod
    def update_creators_file(creator: str) -> bool:
        """
        This function receives a creator and updates the creators file with the given creator.
        :param creator: The creator to be added to the creators file.
        :return: True if the creator was added, False if the creator already exists.
        """
        creators = []
        with open(CREATORS_FILE, mode='a') as creators_file:
            for line in creators_file.readlines():
                creators.append(line)
            if creator not in creators:
                creators_file.write(creator + '\n')
                return True
            else:
                return False

    @staticmethod
    def get_creators() -> list[str]:
        """
        This function returns a list of all the creators in the creators file.
        :return: A list of all the creators in the creators file.
        """
        creators = []
        with open(CREATORS_FILE, mode='r') as creators_file:
            for line in creators_file.readlines():
                creators.append(line)
        return creators

    @staticmethod
    def load_unsolved_card_from_path(path: Path) -> Card:
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

    def save(self, card: Card, solved: bool) -> bool:
        """
        This function receives a card to save and whether it's solved or not.
        Thread sensitive! Use locks.

        :param card: The card object to be saved
        :param solved: Whether the card is solved or not
        :return: True if the card was saved, False otherwise
        """
        self.update_creators_file(card.creator)
        if solved:
            return self.driver.save_solved_card(card)
        else:
            return self.driver.save_unsolved_card(card)

    def find_cards(self, solved: bool, name: str = None, creator: str = None) -> list[Card]:
        if name is None and creator is None:
            print("You must specify either a name or a creator, or both, but not neither.")
            return []
        if solved:
            return self.driver.get_solved_cards(name, creator)
        if name is not None:
            return self.driver.get_unsolved_card_by_name(name)
        else:
            return self.driver.get_unsolved_cards_by_creator(creator)



    #
    # @staticmethod
    # def get_free_id(unsolved_path: Path = None) -> int:
    #     i = 0
    #     if unsolved_path is None:
    #         unsolved_path = Path('../../game')
    #     while True:
    #         if not (unsolved_path / str(i)).exists():
    #             return i
    #         # If the file exists, we'll try the next one
    #         i += 1
    #
    # @staticmethod
    # def save_serialisation(card: bytes, dir_path: Path = None):
    #     """
    #     This function receives a card and a path to which to store it, and stores the card under a new directory in
    #     :param card: The card object to be saved
    #     :param dir_path: The directory in which to store the card serialisation
    #     :return:
    #     """
    #     if dir_path is None:
    #         dir_path = Path('../data')
    #     card_path = dir_path / str(Saver.get_free_id(dir_path))
    #     with open(card_path, mode="wb") as card_file:
    #         card_file.write(card)
    #

