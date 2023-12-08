#!/usr/bin/env python 

import socket
import select
import json
from Game import Game

constants = {
    "SERVER_PORT": 1234,
    "GAME_CODES": {
        "GAME_START": 201,
        "GAME_UPDATE": 202,
        "GAME_END": 203,
        "CLIENT_ACKNOWLEDGE": 204,
        "ERROR": 500
    },
    "PAYLOAD_STATUS": {
        "PENDING": 0,
        "AWAITING_VALIDATION": 1
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
        self.payloads_id = 0
        self.game = Game()

    def __del__(self):
        for client_socket in self.sockets:
            client_socket.close()

    def send_data_to_all_clients(self, code, data):
        for client_socket in self.sockets:
            # Do not send to the server itself
            if client_socket == self.sockets[0]:
                continue

            payload = json.dumps({"id": self.payloads_id, "code": code, "data": data})
            payload_pending_status = constants["PAYLOAD_STATUS"]["PENDING"]
            print("Append", payload)
            self.payloads_to_send.append(
                [self.payloads_id, client_socket, payload.encode("utf-8"), payload_pending_status])
            self.payloads_id += 1

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

    def acknowledge_payload(self, payload):
        for i in range(0, len(self.payloads_to_send)):
            if self.payloads_to_send[i][0] == payload["id"]:
                del self.payloads_to_send[i]
                return

    def handle_client_message(self, client_socket, buffer):
        try:
            data = json.loads(buffer.decode("utf-8"))
            if data["code"] == constants["GAME_CODES"]["CLIENT_ACKNOWLEDGE"]:
                self.acknowledge_payload(data)
        except ValueError:
            print("Invalid data received")

    def begin_game(self):
        # player 1
        self.game.add_player()
        # player 2
        self.game.add_player()
        self.game.place_soldiers_to_initial_pos()
        first_player_soldiers_pos = []
        second_player_soldiers_pos = []
        for soldier in self.game.players[0].soldier_list:
            first_player_soldiers_pos.append((soldier.x, soldier.y))
        for soldier in self.game.players[1].soldier_list:
            second_player_soldiers_pos.append((soldier.x, soldier.y))
        self.send_data_to_all_clients(constants["GAME_CODES"]["GAME_UPDATE"], [])

    def start(self):
        while True:
            try:
                sockets_read_ready, sockets_write_ready, _ = select.select(self.sockets, self.sockets, [])
            except select.error:
                break

            # Read available data
            for socket_read_ready in sockets_read_ready:
                # if socket is the server socket
                if socket_read_ready == self.sockets[0]:
                    client, addr = self.sockets[0].accept()
                    # add new client socket to the list
                    self.sockets.append(client)
                    print("New client connected", addr)
                    # Count server socket (2 player sockets + 1 server socket)
                    if len(self.sockets) == 3:
                        self.send_data_to_all_clients(constants["GAME_CODES"]["GAME_START"], self.game.seed)
                    continue

                client_data = self.read_data_from_client(socket_read_ready)
                print("Received", client_data.decode("utf-8"))
                if client_data is None:
                    # Then client is disconnected
                    self.disconnect_client(socket_read_ready)
                    continue
                # Handle message
                self.handle_client_message(socket_read_ready, client_data)

            # Write payload on ready sockets
            for socket_write_ready in sockets_write_ready:
                for payload_to_send in self.payloads_to_send:
                    if socket_write_ready == payload_to_send[1] and payload_to_send[3] == constants["PAYLOAD_STATUS"]["PENDING"]:
                        socket_write_ready.sendall(payload_to_send[2])
                        payload_to_send[3] = constants["PAYLOAD_STATUS"]["AWAITING_VALIDATION"]


server = Server()
server.start()
