import socket
import struct


from networking.exceptions import DisconnectionException


class Connection:
    sock: socket.socket = None
    host: str
    port: int

    def __init__(self, sock: socket.socket = None):
        self.sock = sock

    def __repr__(self):
        if self.sock is None:
            # If this value is returned, the class likely isn't being used properly.
            return "<Empty Connection obj>"

        local_addr = self.sock.getsockname()
        try:
            remote_addr = self.sock.getpeername()
            return f"<Connection from {local_addr[0]}:{local_addr[1]} to {remote_addr[0]}:{remote_addr[1]}>"
        except OSError:
            # Hasn't connected yet, This shouldn't really happen, but it's good to have
            return f"<Connection object {local_addr[0]}:{local_addr[1]} (Unconnected)>"

    def send_message(self, message: bytes) -> None:
        """
        Sends a message to the connection in the requested format. The function will format the message correctly.
        """
        encoded_data = struct.pack(f">i{len(message)}s", len(message), message)
        self.sock.send(encoded_data)

    def receive_message(self) -> bytes:
        """
        Receives a message from the connection in the requested format, and returns the decoded message.
        """
        length_bytes = self.sock.recv(4)
        if not length_bytes:  # An empty bytes string means the connection was closed
            self.close()
            raise DisconnectionException()
        message_length = struct.unpack("<i", length_bytes)[0]
        # Note the requested message format if this isn't clear.
        raw_msg = self.sock.recv(2**8)
        message = b""

        while len(message) < message_length:
            message += raw_msg
            raw_msg = self.sock.recv(2**8)
            if raw_msg == b'':
                self.close()
                raise DisconnectionException()

        return message

    @classmethod
    def connect(cls, host: str, port: int):
        """
        Connects to a server at host:port, and returns the new object. Note that this function returns a new
        Connection object, and is a class method.
        :param host: The host to connect to
        :param port: The port to connect to
        :return: A new Connection object connected to the specified host and port
        """
        conn_obj = cls()
        conn_obj.sock = socket.socket()
        conn_obj.sock.connect((host, port))
        conn_obj.host = host
        conn_obj.port = port

        return conn_obj

    def close(self):
        self.sock.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
