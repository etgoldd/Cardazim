import argparse
import sys

from networking.connection import Connection
from game.card import Card


def send_data(server_ip: str, server_port: int, data: bytes):
    '''
    Send data to server in address (server_ip, server_port).
    '''
    with Connection.connect(server_ip, server_port) as conn:
        print(f"Sending data...")
        conn.send_message(data)


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument("IPv4", type=str,
                        help="The IP to which you want to send the card")
    parser.add_argument("port", type=str,
                        help="The port to which you want to send the card")
    parser.add_argument("name", type=str,
                        help="The name of the card")
    parser.add_argument("creator", type=str,
                        help="The creator of the card")
    parser.add_argument("image_path", type=str,
                        help="The path to the image file")
    parser.add_argument("riddle", type=str,
                        help="The riddle")
    parser.add_argument("solution", type=str,
                        help="The solution to the riddle")
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    card = Card.create_from_path(args.name, args.creator, args.image_path, args.riddle, args.solution)
    card.encrypt_card()
    try:
        send_data("127.0.0.1", 6666, card.serialize())
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
