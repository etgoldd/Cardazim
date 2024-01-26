import pytest
import socket
import struct

from networking.connection import Connection
from game.card import Card

CLIENT_TEST_CARD_NAME = "test"


class MockSocket:
    sent_data = []
    addr = None
    already_received = False

    def connect(self, addr):
        self.addr = addr

    def send(self, data):
        self.sent_data.append(data)

    def recv(self, size):
        if self.already_received:
            return b""
        self.already_received = True
        card = get_card(CLIENT_TEST_CARD_NAME)
        card.encrypt_card()
        card_serialisation = card.serialise()
        return card_serialisation


    def close(self):
        pass


@pytest.fixture
def mock_socket(monkeypatch):
    monkeypatch.setattr(socket, "socket", MockSocket)


def get_card(name: str) -> Card:
    # Adding the name so that we can create a few copies
    name = name
    creator = "testy mctestface"
    riddle = "i <3 tests"
    solution = "test" * 4
    path = "/home/mrsandman/mystuff/arazim/CardazimProject/Cardazim/networking/cheese.jpg"
    return Card.create_from_path(name=name, creator=creator, riddle=riddle, solution=solution, path=path)


def test_connect(mock_socket):
    connection_obj = Connection.connect("127.0.0.1", 6666)
    assert (connection_obj.host, connection_obj.port) == ("127.0.0.1", 6666)
    with connection_obj as connection:
        card = get_card("sometest")
        card.encrypt_card()
        # Must encrypt the card, otherwise there will be no key_hash.
        card_serialisation = card.serialise()
        connection.send_message(card_serialisation)

        serialisation_message = struct.pack(f">i{len(card_serialisation)}s", len(card_serialisation), card_serialisation)
        assert connection_obj.sock.sent_data == [serialisation_message]



