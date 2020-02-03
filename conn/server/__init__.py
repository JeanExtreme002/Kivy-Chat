from conn import Connection
from threading import Thread
import socket


class Server(Connection):

    __connections = []


    def __init__(self, address, username):

        self.username = username
        self.socket = socket.socket()
        self.socket.bind(address)
        self.socket.listen(0)


    def __acceptConnections(self):

        while self.__running:
            try: connection, address = self.socket.accept()
            except: break
            
            user = {"address":address, "connection":connection, "online": True}
            self.__connections.append(user)

            listener = Thread(target = lambda: self.__messageListener(user))
            listener.start()
        self.__running = False


    def __messageListener(self, user):

        connection = user["connection"]
        username = connection.recv(1024).decode()
        connection.settimeout(5)

        self.__sendAll(username + " joined the chat.")

        while user["online"]:
            try: 
                message = connection.recv(1024)
                if not message: break

            except socket.timeout: continue
            except: break

            if message: 
                self.__sendAll(username + " : " + message.decode(), author = user)

        connection.close()
        self.__connections.remove(user)
        self.__sendAll(username + " has left the chat.", author = user)


    def __sendAll(self, message, author = None):

        self.messageCallback(message)

        for user in self.__connections:

            if not user is author:

                try:
                    user["connection"].send((message + self.separator).encode())
                except:
                    user["online"] = False


    def close(self):

        for user in self.__connections:
            user["online"] = "False"
            user["connection"].close()
        self.socket.close()
        self.__running = False


    def run(self, messageCallback):

        self.__running = True
        self.messageCallback = messageCallback
        Thread(target = self.__acceptConnections).start()


    def send(self, message):
        self.__sendAll(self.username + " : " + message)



