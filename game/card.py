from __future__ import annotations
from typing import Optional, Any
from PIL import Image
import struct
import json

from game.crypt_image import CryptImage


class Card:
    # It's questionable that Card has serialisation methods, shouldn't that be left
    # to some sort data management bridge to do?
    name: str
    creator: str
    image: CryptImage
    image_path: str
    riddle: str
    solution: Optional[str] = None

    def __repr__(self):
        return f"<Card {self.name} by {self.creator}>"

    def __str__(self):
        card_str = f"Card {self.name} by {self.creator}\n"
        card_str += f"\tRiddle: {self.riddle}\n"
        if self.solution:
            card_str += f"\tSolution: {self.solution}\n"
        else:
            card_str += "\tSolution: unsolved\n"

    def encrypt_card(self):
        """
        Encrypts the card's image with the solution as the key.
        """
        self.image.encrypt(self.solution)

    def decrypt_card(self, key: str) -> bool:
        """
        Attempts to decrypt the card's image with given key. Returns True if the decryption succeeded,
        and False otherwise.
        """
        decrypt_success = self.image.decrypt(key)
        if decrypt_success:
            self.solution = key
        return decrypt_success

    def set_image(self, image: Image.Image):
        """
        Sets the card's image to the given image. To allow needed access.
        """
        self.image.set_image(image)

    @classmethod
    def create_from_path(cls, name: str, creator: str, path: str, riddle: str, solution: Optional[str] = None) -> Card:
        card_obj = cls()
        card_obj.name = name
        card_obj.creator = creator
        card_obj.image = CryptImage()
        card_obj.image_path = path
        card_obj.image.set_image(Image.open(path))
        card_obj.image.key_hash = None

        card_obj.riddle = riddle
        card_obj.solution = solution
        return card_obj

    def _generate_struct_format(self) -> str:
        name_format = f"i{len(self.name)}s"
        creator_format = f"i{len(self.creator)}s"
        image_size = self.image.image.size
        image_pixels = image_size[0] * image_size[1] * 3
        image_format = f"ii{image_pixels}s"
        hash_format = f"32s"
        riddle_format = f"i{len(self.riddle)}s"
        struct_format = "<" + name_format + creator_format + image_format + hash_format + riddle_format
        return struct_format

    def _generate_format_parameters(self) -> tuple:
        image_size = self.image.image.size
        return (len(self.name),
                bytes(self.name, 'utf8'),
                len(self.creator),
                bytes(self.creator, 'utf8'),
                image_size[0],
                image_size[1],
                self.image.image.tobytes(),
                self.image.key_hash,
                len(self.riddle),
                bytes(self.riddle, 'utf8'),
                )

    def serialise(self) -> bytes:
        """
        This returns the serialization of the card object.
        """
        struct_format = self._generate_struct_format()
        serialisation = struct.pack(struct_format, *self._generate_format_parameters())
        return serialisation

    @staticmethod
    def extract_format(data: bytes, struct_format: str, field_size: int) -> tuple[Any, bytes]:
        """
        This method takes in a serialization of a card object, and extracts the requested field from it, according to
        the format and field size given. Also returns the data without the extracted field.
        :param data: The serial of the card object.
        :param struct_format: The format of the field. (According to the struct module)
        :param field_size: The size of the field.
        """
        return struct.unpack(struct_format, data[:field_size])[0], data[field_size:]

    @classmethod
    def deserialize(cls, data: bytes) -> Card:
        """
        This method takes in a serialization of a card object and returns a new card object.
        :param data: The serial of the card object.
        :return: The new object.
        """
        # This function is a bit gross, it can be made cleaner, but it really wouldn't be time effective to do that.
        card_obj = cls()
        # FIELDS:
        # name
        name_length, data = cls.extract_format(data, "<i", 4)
        name_bytes, data = cls.extract_format(data, f"{name_length}s", name_length)
        card_obj.name = name_bytes.decode('utf8')
        # creator
        creator_length, data = cls.extract_format(data, "<i", 4)
        creator_bytes, data = cls.extract_format(data, f"{creator_length}s", creator_length)
        card_obj.creator = creator_bytes.decode('utf8')
        # image
        height, data = cls.extract_format(data, "<i", 4)
        width, data = cls.extract_format(data, "<i", 4)
        image_data_size = width * height * 3
        image_data, data = cls.extract_format(data, f"{image_data_size}s", image_data_size)
        # key_hash
        key_hash, data = cls.extract_format(data, f"32s", 32)
        # creating the image object
        card_obj.image = CryptImage((height, width), image_data, key_hash)
        # riddle
        riddle_length, data = cls.extract_format(data, f"<i", 4)
        riddle_bytes, data = cls.extract_format(data, f"{riddle_length}s", riddle_length)
        card_obj.riddle = riddle_bytes.decode('utf8')

        return card_obj

    def get_attributes(self):
        # May turn this into a property later, no need currently
        return {
            "name": self.name,
            "creator": self.creator,
            "riddle": self.riddle,
            "solution": self.solution,
            "path": self.image_path,
        }
    def generate_metadata_json(self) -> str:
        """
        This function receives a card and returns a json-format string of its metadata.
        :return: Whether the generation succeeded
        """

        try:
            encoder = json.JSONEncoder()
            card_json = encoder.encode(self.get_attributes())
        except TypeError as e:
            print(
                f"Something has gone wrong while encoding the card's metadata, here's the card: \n{str(self)} \n raising error...")
            raise e
        except ValueError as e:
            print(
                f"Something has gone wrong while encoding the card's metadata, here's the card: \n{str(self)} \n raising error...")
            raise e

        return card_json

    @classmethod
    def load_from_metadata(cls, metadata: dict) -> Card:
        """
        This function receives a metadata dictionary and returns a card object.
        :param metadata:
        :return:
        """
        new_card = cls()
        try:
            new_card.name = metadata["name"]
            new_card.creator = metadata["creator"]
            new_card.riddle = metadata["riddle"]
            new_card.solution = metadata["solution"]
            new_card.image_path = metadata["path"]
        except KeyError as e:
            print("metadata file was poorly generated, and a card couldn't be loaded \n"
                  f"Offending metadata: \n {metadata}")
            raise e
        try:
            image = Image.open(new_card.image_path)
        except FileNotFoundError as e:
            print(f"Path found in metadata file doesn't exist. Here's the metadata \n"
                  f"f{metadata}")
            raise e
        new_card.set_image(image)
        return new_card

    def get_id(self) -> str:
        # Using this instead of just the name, in case the name is really long or not
        # very unique
        return str(hash(self.name + self.creator))


if __name__ == '__main__':
    name = "test"
    creator = "testy mctestface"
    riddle = "i <3 tests"
    solution = "test"*4
    path = "../networking/cheese.jpg"

    card = Card.create_from_path(name=name, creator=creator, riddle=riddle, solution=solution, path=path)
    card.image.image.show()
    card.image.encrypt(card.solution)
    data = card.serialise()
    card2 = Card.deserialize(data)
    card2.image.image.show()
    if card2.image.decrypt(solution):
        card2.solution = solution
    print(repr(card), repr(card2))
    assert (repr(card) == repr(card2))
    card2.image.image.show()
