from __future__ import annotations
from Crypto.Cipher import AES
from typing import Optional
from PIL import Image
import hashlib


class CryptImage:
    image: Image.Image = None
    key_hash: Optional[bytes]

    def __init__(self,
                 image_size: Optional[tuple[int, int]] = None,
                 image_data: Optional[bytes] = None,
                 key_hash: Optional[bytes] = None
                 ):
        if image_data is None:
            self.image = None
        else:
            height, width = image_size
            self.image = Image.new('RGB', (height, width))
            self.image.frombytes(image_data)
        self.key_hash = key_hash

    def set_image(self, image: Image.Image):
        self.image = image

    @classmethod
    def create_from_path(cls, path: str) -> Optional[CryptImage]:
        try:
            image = Image.open(path)
        except FileNotFoundError:
            print(f"File '{path}' doesn't exist, oops!")
            return None
        crypt_image_obj = cls()
        crypt_image_obj.image = image
        crypt_image_obj.key_hash = None
        return crypt_image_obj

    @staticmethod
    def _generate_hash_key(key: bytes) -> bytes:
        return hashlib.sha256(hashlib.sha256(key).digest()).digest()

    def encrypt(self, key: str):
        """
        The function encrypts the image using AES in EAX mode, with the given key. Updates the key_hash property too.
        :param key: The key with which the image will be encrypted
        :return:
        """
        key_bytes = key.encode('utf8')
        self.key_hash = self._generate_hash_key(key_bytes)
        image_data = self.image.tobytes()
        cipher = AES.new(key_bytes, AES.MODE_EAX, nonce=b'arazim')
        encrypted_image_data = cipher.encrypt(image_data)
        self.image.frombytes(encrypted_image_data)

    def decrypt(self, key: str) -> bool:
        """
        :param key:
        :return: True if decryption succeeded, False otherwise
        """
        # Testing the key's correctness, if it's wrong, we won't bother trying to decrypt the image.
        key_bytes = key.encode('utf8')
        if self._generate_hash_key(key_bytes) != self.key_hash:
            return False
        ciphertext = self.image.tobytes()
        cipher = AES.new(bytes(key, 'utf8'), AES.MODE_EAX, nonce=b'arazim')
        image_data = cipher.decrypt(ciphertext)
        self.image.frombytes(image_data)
        return True

