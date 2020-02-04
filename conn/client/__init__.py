from conn import Connection
from threading import Thread 
import socket


class Client(Connection):

    """
    Classe para conectar-se a um servidor.
    """

    def __init__(self, address: tuple, username: str):

        """
        Address: Endereço do servidor
        Username: Nome de usuário
        """

        self.username = username
        self.socket = socket.socket()
        self.socket.connect(address)
        self.socket.send(username.encode())


    def __messageListener(self):

        """
        Recebe as mensagens do servidor.
        """

        self.socket.settimeout(self.timeout)

        while self.__running:
            try:
                message = self.socket.recv(1024)
                if not message: break

            except socket.timeout:
                continue

            except:
                break

            messages = message.decode().split(self.separator)

            for message in messages:
                self.messageCallback(message)

        self.messageCallback(self.warningMessages["connection_lost"])
        self.__running = False


    def close(self) -> None:

        """
        Encerra conexão com o servidor.
        """

        self.__running = False
        self.socket.close()


    def run(self, messageCallback) -> None:

        """
        Inicia o recebimento de mensagens.
        """

        self.__running = True
        self.messageCallback = messageCallback
        Thread(target = self.__messageListener).start()


    def send(self, message: str) -> None:
        
        """
        Envia uma mensagem ao servidor.
        """

        if self.__running:

            try: self.socket.send(message.encode())
            except: self.__running = False

            self.messageCallback(self.username + " : " + message)