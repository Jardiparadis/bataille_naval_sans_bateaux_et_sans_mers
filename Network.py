import socket
import select
from queue import Queue, Empty
from threading import Thread

SERVER_HOST = "192.168.1.223"
SERVER_PORT = 1234


class Network:
    def __init__(self, send_queue, receive_queue):
        self.send_queue = send_queue
        self.receive_queue = receive_queue
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((SERVER_HOST, SERVER_PORT))
        except socket.error as error:
            print(f"Cannot connect to {SERVER_HOST}:{SERVER_PORT}: {error}")

    def receive_data(self):
        try:
            received_data = self.receive_queue.get(block=False)
            return received_data
        except Empty:
            return None

    def send_data(self, data):
        self.send_queue.put(data)

    def run(self):
        while True:
            try:
                sockets_read_ready, sockets_write_ready, _ = select.select([self.socket], [self.socket], [])
            except select.error:
                break

            # Read available data
            for socket_read_ready in sockets_read_ready:
                buffer = socket_read_ready.recv(256)
                self.send_data(buffer)

            # Write payload on ready sockets
            for socket_write_ready in sockets_write_ready:
                data_to_send = self.receive_data()
                if data_to_send:
                    socket_write_ready.sendall(data_to_send)


def start_network_thread(send_queue, receive_queue):
    network = Network(send_queue, receive_queue)
    network.run()


class NetworkManager:
    def __init__(self):
        self.send_queue = Queue()
        self.receive_queue = Queue()
        self.thread = Thread(target=start_network_thread, args=(self.receive_queue, self.send_queue))
        self.thread.start()

    def fetch_message(self):
        try:
            return self.receive_queue.get(block=False)
        except Empty:
            return None

    def send_message(self, message):
        self.send_queue.put(message)


# Exemple
"""
net = NetworkManager()

while True:
    d = net.fetch_message()
    if d:
        print("=>", d)
        net.send_message(b"test")
"""