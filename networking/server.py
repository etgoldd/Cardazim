from typing import NoReturn
import argparse
import struct
import socket


def process_message(raw_msg: bytes) -> str:
    return raw_msg.decode('utf8')

def decode_length(raw_length: bytes) -> int:
    return struct.unpack("<i", raw_length)[0]


def run_server(server_ip: str, server_port: int) -> NoReturn:
    server_sock = socket.socket()
    server_sock.bind((server_ip, server_port))

    while True:
        server_sock.listen(1)
        conn_sock, conn_address = server_sock.accept()
        msg_len = decode_length(conn_sock.recv(4))
        raw_msg = conn_sock.recv(msg_len)
        print(f"received message: {process_message(raw_msg)}")
        conn_sock.detach()
        # TODO FINISH ME


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

