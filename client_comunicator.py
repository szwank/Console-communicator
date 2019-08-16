import socket
import threading
from utils import HashPassword, DisplayClientLogs

class UTP_client():

    def __init__(self, server_ip, server_port, password, name='User'):
        self.__server_ip = server_ip
        self.__server_port = server_port
        self.__name = name

        self.__password_hash = HashPassword.hash_password(password)

        self.__connection = self.__create_connection_with_server()

        self.__receive_message_thread = threading.Thread(target=self.__receive_message, args=())

        self.__stop_client = threading.Event()

    def __receive_message(self):
        while not self.__stop_client.is_set():
            try:
                message, address = self.__connection.recvfrom(1024)
                if address == (self.__server_ip, self.__server_port):
                    thread = threading.Thread(target=self.__handle_message, kwargs={'message': message})
                    thread.start()
            except:
                pass

    def __handle_message(self, message):
        self.__print_recived_message(message.decode())


    def send_message(self, message):
        if message is "RECONNECT":
            self.__connect_to_server()
        else:
            try:
                self.__send_message_to_server(self.__name + ": " + message)
            except:
                pass

    def __create_connection_with_server(self):
        connection = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        connection.bind((self.__server_ip, 0))
        connection.setblocking(False)
        return connection

    def __connect_to_server(self):
        self.__send_message_to_server("PASSWORD:" + self.__password_hash)

    def start(self):
        self.__connect_to_server()
        self.__receive_message_thread.start()

    def __send_message_to_server(self, message):
        self.__connection.sendto(message.encode(), (self.__server_ip, self.__server_port))

    def __print_recived_message(self, message):
        DisplayClientLogs.print_message(message)

    def stop(self):
        self.__stop_client.set()
        self.__print_client_log('Client stopped')

    def __print_client_log(self, message):
        DisplayClientLogs.print_client_log(message)



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
    client.stop()

if __name__ == '__main__':
    main()