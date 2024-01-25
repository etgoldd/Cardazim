from typing import NoReturn
import threading
import argparse


from networking.listener import Listener
from networking.connection import Connection
from game.card import Card


def run_server(server_ip: str, server_port: int) -> NoReturn:
    with Listener(server_ip, server_port) as listener:
        while True:
            conn = listener.accept()
            # Why did we demand connection to be a context manager? That doesn't work with multithreading very well
            connection_thread = threading.Thread(target=manage_conn, args=[conn])
            connection_thread.start()


def manage_conn(connection: Connection):
    with connection as conn:
        message = conn.receive_message()
        card = Card.deserialize(message)
        print(f"received message: {repr(card)}")


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("IPv4",
                        type=str,
                        help="The server's IPv4 address")
    parser.add_argument("port",
                        type=int,
                        help="The port the server will listen on")
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    server_ip = args.IPv4
    server_port = args.port

    run_server(server_ip, server_port)

