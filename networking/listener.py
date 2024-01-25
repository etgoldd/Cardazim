import socket

from networking.connection import Connection


class Listener:
    def __init__(self, host: str, port: int, backlog: int = 1000):
        self.backlog = backlog
        self.connection = None
        self.sock = socket.socket()
        self.host = host
        self.port = port

    def __repr__(self):
        return f"Listener(host={self.connection.host}, port={self.connection.port}, backlog={self.backlog})"

    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.backlog)

    def stop(self):
        self.sock.close()
        # Note: the listener can close while the connection stays open.

    def accept(self) -> Connection:
        """
        Accepts a connection, and returns a Connection object representing the connection.
        :return: A new connection
        """
        remote_socket, _ = self.sock.accept()
        self.connection = Connection(remote_socket)
        return self.connection

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()



