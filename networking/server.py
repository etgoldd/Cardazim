from typing import NoReturn
import threading
import argparse
import struct
import socket


def process_message(raw_msg: bytes) -> str:
    return raw_msg.decode('utf8')

def decode_length(raw_length: bytes) -> int:
    print(raw_length)
    return struct.unpack("<i", raw_length)[0]


def run_server(server_ip: str, server_port: int) -> NoReturn:
    server_sock = socket.socket()
    server_sock.bind((server_ip, server_port))

    while True:
        server_sock.listen(10)  # 10 - To avoid multiple connections being dropped if attempted at the same time.
        conn_sock, conn_address = server_sock.accept()

        conn_thread = threading.Thread(target=manage_conn, args=[conn_sock])
        conn_thread.start()


def manage_conn(conn_sock: socket.socket):
    while True:
        message_length_bytes = conn_sock.recv(4)
        if not message_length_bytes:  # Empty byte string means connection was closed
            break
        msg_len = decode_length(message_length_bytes)
        raw_msg = conn_sock.recv(msg_len)
        decoded_message = process_message(raw_msg)
        print(f"received message: {decoded_message}")
        # This wasn't requested, but it feels necessary.
        if decoded_message == "bye.":
            break
    conn_sock.detach()


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

