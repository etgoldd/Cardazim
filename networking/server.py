from typing import NoReturn
from pathlib import Path
import threading
import argparse


from networking.listener import Listener
from networking.connection import Connection
from game.saver import Saver
from game.card import Card


def run_server(server_ip: str, server_port: int, card_dir: str) -> NoReturn:
    io_lock = threading.Lock()
    with Listener(server_ip, server_port) as listener:
        while True:
            conn = listener.accept()
            # Why did we demand connection to be a context manager? That doesn't work with multithreading very well
            connection_thread = threading.Thread(target=manage_conn, args=[conn, card_dir, io_lock])
            connection_thread.start()


def manage_conn(connection: Connection, card_dir: Path, lock: threading.Lock):
    """
    This function manages a connection with a client. It saves the card it receives to the directory specified.
    :param connection: The connection with the client
    :param card_dir: The directory in which to save the card
    :param lock: threading lock, this function is thread sensitive
    :return:
    """
    with connection as conn:
        card_serialisation = conn.receive_message()
        Saver.save_serialisation(card_serialisation, card_dir)
    lock.acquire()
    print(f"Received card.")
    lock.release()


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("IPv4",
                        type=str,
                        help="The server's IPv4 address")
    parser.add_argument("port",
                        type=int,
                        help="The port the server will listen on")
    parser.add_argument("card_dir",
                        type=str,
                        help="The directory in which to store the cards")
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    server_ip = args.IPv4
    server_port = args.port
    card_dir = args.card_dir
    run_server(server_ip, server_port, card_dir)

