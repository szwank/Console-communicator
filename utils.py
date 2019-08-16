import time
import hashlib
import uuid

class DisplayClientLogs():
    @staticmethod
    def print_message(message):
        print(message)

    @staticmethod
    def print_client_log(message):
        print(str(time.ctime(time.time())) + ": " + str(message))

class DisplayServerLogs:

    @staticmethod
    def print_message_log(message, address):
        print(str(time.ctime(time.time())) + ": Recived message from " + str(address) + ": " + str(message))


    @staticmethod
    def print_server_log(message):
        print(str(time.ctime(time.time())) + ": " + str(message))


class HashPassword:

    @staticmethod
    def check_password(hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

    @staticmethod
    def hash_password(password):
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt