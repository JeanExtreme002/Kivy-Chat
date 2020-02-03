from conn import Connection
from threading import Thread 
import socket


class Client(Connection):

    def __init__(self, address, username):

        self.username = username
        self.socket = socket.socket()
        self.socket.connect(address)
        self.socket.send(username.encode())


    def __messageListener(self):

        self.socket.settimeout(5)

        while self.__running:
            try:
                message = self.socket.recv(1024)
                if not message: break

            except socket.timeout:
                continue

            except:
                break

            if message:
                messages = message.decode().split(self.separator)

                for message in messages:
                    self.messageCallback(message)

        self.messageCallback("Lost connection to the server.")
        self.__running = False


    def close(self):
        self.__running = False
        self.socket.close()


    def run(self, messageCallback):

        self.__running = True
        self.messageCallback = messageCallback
        Thread(target = self.__messageListener).start()


    def send(self, message):

        if self.__running:
            try:
                self.socket.send(message.encode())
            except:
                self.__running = False
            self.messageCallback(self.username + " : " + message)