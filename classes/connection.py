from config.settings import STRUCT_PACK_FORMAT
import socket
import struct


class Connection(socket.socket):
    def recvall(self, bytes_to_read: int) -> (bytearray | None):
        data = bytearray()

        # Get byte by byte the content
        while len(data) < bytes_to_read:
            packet = self.recv(bytes_to_read - len(data))
            if not packet:
                return None
            
            data.extend(packet)
        
        return data

    def send_decoded(
            self, 
            message: str = "", 
            *,
            encode_format: str = "utf-8"
        ) -> None:
        return self.send_encoded(
            message=message.encode(encoding=encode_format)
        )

    def send_encoded(self, message: bytes) -> None:
        # Add the size of the message at the beginning of the output
        output = struct.pack(
            STRUCT_PACK_FORMAT, 
            len(message)
        ) + message
        
        self.sendall(output)

    def recv_decoded(self, *, decode_format: str = "utf-8") -> (str | None):
        received = self.recv_encoded()
        if not received:
            return None

        return received.decode(encoding=decode_format)

    def recv_encoded(self) -> (bytearray | None):
        # Get the size of the message
        raw_message_len = self.recvall(
            bytes_to_read=4
        )

        if not raw_message_len:
            return None

        message_len = struct.unpack(
            STRUCT_PACK_FORMAT, 
            raw_message_len
        )[0]

        # Return the rest of the message
        return self.recvall(
            bytes_to_read=message_len
        )
