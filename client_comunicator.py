import socket
import threading
import time
import hashlib
import uuid

class UTP_client():

    def __init__(self, server_ip, server_port, password, name='User'):
        self.server_ip = server_ip
        self.server_port = server_port
        self.name = name

        self.password_hash = self.__hash_password(password)

        self.__establish_connection_with_server()

        self.receive_message_thread = threading.Thread(target=self.__receive_message, args=())

        self.stop_client = threading.Event()

    def __receive_message(self):
        while not self.stop_client.is_set():
            pass

    def send_message(self, message):
            try:
                self.__send_message_to_server(self.name + ": " + message)
            except:
                pass

    def __establish_connection_with_server(self):
        self.connection = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.connection.bind((self.server_ip, 0))
        self.connection.setblocking(False)

    def __connect_to_server(self):
        self.__send_message_to_server(self.password_hash)

    def start(self):
        self.__connect_to_server()
        self.receive_message_thread.start()

    def __hash_password(self, password):
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


    def __send_message_to_server(self, message):
        self.connection.sendto(message.encode(), (self.server_ip, self.server_port))

class DisplayLogs():
    @staticmethod
    def print_message(message, name):
        print(name + ": " + message)

    @staticmethod
    def print_client_log(message):
        print(str(time.ctime(time.time())) + ": " + str(message))


def main():
    # IP = input("Enter server IP -> ")
    # PORT = input("Enter server port -> ")
    # NAME = input("Enter nick name -> ")
    IP = '127.0.0.1'
    PORT = 5000
    NAME = 'szwank'

    client = UTP_client(IP, PORT, 'password', NAME)
    client.start()

    message = input("--> ")
    while message != 'q':
        client.send_message(message)
        message = input("--> ")


if __name__ == '__main__':
    main()