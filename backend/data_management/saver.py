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
        with open(CREATORS_FILE, mode='r') as creators_file:
            # readlines was being weird
            creators = creators_file.read().split("\n")
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

if __name__ == '__main__':
    saver = Saver()
    name = "test"
    creator = "testy mctestface"
    riddle = "i <3 tests"
    solution = "test" * 4
    path = "/home/mrsandman/mystuff/arazim/CardazimProject/Cardazim/networking/cheese.jpg"
    card = Card.create_from_path(name=name, creator=creator, riddle=riddle, solution=solution, path=path)
    saver.save(card, True)