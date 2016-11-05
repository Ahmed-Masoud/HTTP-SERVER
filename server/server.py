import socket
from threading import *
import Parser


class Server:
    def __init__(self, host, port, num_of_requests):
        # create socket for TCP Connection
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind to the port
        self.socket.bind((host, port))
        # queue up to 5 requests
        self.socket.listen(num_of_requests)

        self.threads = []

    @staticmethod
    def send_file_to_client(client_socket, file_path):
        try:
            f = open(file_path, 'r')

            client_socket.send('HTTP/1.1 200 OK')

            while True:
                data = f.readline(512)
                if not data:
                    break
                client_socket.send(data)
            f.close()

        except IOError:
            client_socket.send("404 Not Found")
            client_socket.close()
            return

    @staticmethod
    def get_file_from_client(client_socket, file_path):
        new_file = open(file_path, "w+")
        client_socket.send("receiving")
        while True:
            msg = client_socket.recv(512)
            if not msg:
                break
            print(msg)
            new_file.write(msg)
        new_file.close()

    def __handle_request(self, client_socket, addr):

        print('Got a connection from %s' % str(addr))

        # receive message from client
        client_msg = client_socket.recv(512)
        print(client_msg + '\n')

        # parse HTTP request to return an abject with HTTP Variables
        parsed_msg = Parser.http(client_msg)

        if parsed_msg:
            if parsed_msg.method == 'GET':
                self.send_file_to_client(client_socket, parsed_msg.file_path)
            elif parsed_msg.method == 'POST':
                self.get_file_from_client(client_socket, parsed_msg.file_path)

        else:
            client_socket.send("Error: Unknown Command")

        client_socket.close()

    def start(self):
        while True:
            # establish a connection
            client_socket, addr = self.socket.accept()
            self.threads.append(Thread(target=self.__handle_request(client_socket, addr)))
            self.threads[-1].start()
            self.threads[-1].join()
