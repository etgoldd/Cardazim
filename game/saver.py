    from game.card import Card


class Saver:

    @staticmethod
    def save(card: Card, dir_path: str = '.'):
        """
        This function receives a card and a path to which to store it, and stores the serial of the card in a file
        under the path given.
        Not thread-safe! Use locks.

        :param card: The card object to be saved
        :param dir_path: The directory in which to store the card serial
        """
        file_path = f"{dir_path}/{card.name}"
        card_data = card.serialize()
        with open(file_path, mode="wb") as card_file:
            card_file.write(card_data)
