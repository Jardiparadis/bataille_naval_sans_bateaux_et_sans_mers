import socket
import select
import json

constants = {
    "SERVER_PORT": 1234,
    "GAME_CODES": {
        "GAME_START": 201,
        "GAME_UPDATE": 202,
        "GAME_END": 203,
        "ERROR": 500
    }
}


class Server:
    def __init__(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((socket.gethostname(), constants["SERVER_PORT"]))
        server_socket.setblocking(False)
        server_socket.listen(2)
        self.sockets = [server_socket]
        self.payloads_to_send = []

    def __del__(self):
        for client_socket in self.sockets:
            client_socket.close()

    def send_data_to_all_clients(self, code, data):
        payload = json.dumps({code: code, data: data})
        for client_socket in self.sockets:
            self.payloads_to_send.append((client_socket, bytes(payload, 'utf-8')))

    def read_data_from_client(self, client_socket):
        try:
            buffer = client_socket.recv(256)
            if len(buffer) == 0:
                return None
            return buffer
        except socket.error:
            # There is no data to read
            return None

    def disconnect_client(self, client_socket):
        client_socket.close()
        self.sockets.remove(client_socket)

    def handle_client_message(self, client_socket, buffer):
        pass

    def start(self):
        while True:
            try:
                sockets_read_ready, sockets_write_ready, _ = select.select(self.sockets, self.sockets, [])
            except select.error:
                break

            for socket_read_ready in sockets_read_ready:
                # if socket is the server socket
                if socket_read_ready == self.sockets[0]:
                    client, _ = self.sockets[0].accept()
                    # add new client socket to the list
                    self.sockets.append(client)
                    if len(self.sockets) == 2:
                        self.send_data_to_all_clients(constants["GAME_CODES"]["GAME_START"], "start")
                    continue

                client_data = self.read_data_from_client(socket_read_ready)
                if client_data is None:
                    # Then client is disconnected
                    self.disconnect_client(socket_read_ready)
                    continue
                # Handle message
                self.handle_client_message(socket_read_ready, client_data)

            for socket_write_ready in sockets_write_ready:
                for payload_to_send in self.payloads_to_send:
                    if socket_write_ready == payload_to_send[0]:
                        socket_write_ready.sendall(payload_to_send[1])
                        self.payloads_to_send.remove(payload_to_send)


# Error { code: 500, data: "" }
# Game { code: 200, data:"" }

server = Server()
server.start()
