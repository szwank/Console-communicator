import socket
from utils import DisplayServerLogs, HashPassword
import threading


class UTP_server():
    def __init__(self, ip, port, password=None):
        self.__connected_clients = []
        self.__client_thread = []

        self.__password = self.__hash_password(password)

        self.__connection = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.__connection.bind((ip, port))
        self.__connection.setblocking(False)

        self.__handle_incoming_data_thread = threading.Thread(target=self.__listen_for_incoming_messages, args=())

        self.__stop_server = threading.Event()

    def start(self):
        self.__handle_incoming_data_thread.start()
        self.__print_server_log("Server started")

    def __hash_password(self, password):
        if password is None:
            return None
        else:
            return HashPassword.hash_password(password)

    def __password_is_correct(self, client_password):
        return HashPassword.check_password(self.__password, client_password)

    def ___add_client(self, address):
        self.__connected_clients.append(address)
        self.__print_server_log('Added client ' + str(address))

    def __handle_message(self, message, address):
        if address in self.__connected_clients:
            self.__print_message_log(message, address)
            self.__send_message_to_others_users(message=message, sender_adress=address)
        else:
            if message.decode().split(':')[0] == 'PASSWORD':
                if self.__password is None or self.__password_is_correct(message.decode().split(':')[1]):
                    self.___add_client(address)

    def __listen_for_incoming_messages(self):
        while not self.__stop_server.is_set():
            try:
                message, address = self.__connection.recvfrom(1024)
                arguments = {'message': message, 'address': address}
                thread = threading.Thread(target=self.__handle_message, kwargs=arguments)
                thread.start()
            except:
                pass

    def __send_message_to_others_users(self, message, sender_adress):
        for address in self.__connected_clients:
            if address != sender_adress:
                self.__connection.sendto(message, address)

    def __print_message_log(self, message, address):
        DisplayServerLogs.print_message_log(message.decode(), address)

    def __print_server_log(self, message):
        DisplayServerLogs.print_server_log(message)

    def close(self):
        self.__stop_server.set()

        self.__handle_incoming_data_thread.join()

        DisplayServerLogs.print_server_log("Server closed")


def main():
    IP = '127.0.0.1'
    PORT = 5000

    server = UTP_server(IP, PORT)

    server.start()
    command = input()
    while command != 'q':
        command = input()

    server.close()

if __name__ == '__main__':
    main()

