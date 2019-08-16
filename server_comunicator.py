import socket
import time
import threading

class UTP_server():
    def __init__(self, ip, port):
        self.connected_clients = []
        self.client_thread = []

        self.connection = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.connection.bind((ip, port))
        self.connection.setblocking(False)

        self.listen_for_new_connections = threading.Thread(target=self.__listen_for_new_clients, args=())

        self.stop_server = threading.Event()

    def start(self):
        self.listen_for_new_connections.start()
        self.__print_server_log("Server started")



    def ___add_client(self, address):
        self.connected_clients.append(address)
        self.__add_thread_for_client(address)

    def __listen_for_new_clients(self):
        while not self.stop_server.is_set():
            try:
                _, address = self.connection.recvfrom(1024)     # _ omit one received variable
                if address not in self.connected_clients:
                    self.___add_client(address)
                    self.__print_server_log('Added client ' + str(address))
            except:
                pass

    def __add_thread_for_client(self, client_address):
        self.client_thread.append(threading.Thread(target=self.__listen_client_messages, kwargs={'client_address':client_address}))
        self.client_thread[-1].start()

    def __listen_client_messages(self, client_address):
        while not self.stop_server.is_set():
            try:
                message, address = self.connection.recvfrom(1024)
                if address == client_address and address in self.connected_clients:
                    self.__print_message_log(message.decode(), address)
            except:
                pass

    def __resend_message_to_others_users(self, message, sender_adress):
        for address in self.connected_clients:
            if address != sender_adress:
                self.connection.sendto(message.encode(), address)

    def __print_message_log(self, message, address):
        Display_logs.print_message_log(message, address)

    def __print_server_log(self, message):
        Display_logs.print_server_log(message)

    def close(self):
        self.stop_server.set()
        for thread in self.client_thread:
            thread.join()

        self.listen_for_new_connections.join()

        Display_logs.print_message_log("Server_closed")

class Display_logs:

    @staticmethod
    def print_message_log(message, address):
        print(str(time.ctime(time.time())) + ": Recived message from " + str(address) + ": " + str(message))


    @staticmethod
    def print_server_log(message):
        print(str(time.ctime(time.time())) + ": " + str(message))






def main():
    IP = '127.0.0.1'
    PORT = 5000

    server = UTP_server(IP, PORT)

    server.start()


if __name__ == '__main__':
    main()

