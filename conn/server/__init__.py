from conn import Connection
from threading import Thread
import socket


class Server(Connection):

    """
    Classe para criar e gerenciar um servidor.
    """

    __connections = []


    def __init__(self, address: tuple, username: str):

        self.username = username
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(address)
        self.socket.listen(0)


    def __acceptConnections(self):

        """
        Aguarda e aceita solicitações de conexão com o servidor.
        """

        while self.__running:

            try: connection, address = self.socket.accept()
            except: break
            
            user = {"address":address, "connection":connection, "online": True, "username": None}
            self.__connections.append(user)

            listener = Thread(target = lambda: self.__messageListener(user))
            listener.start()

        self.__running = False


    def __messageListener(self, user):

        """
        Recebe as mensagens de um cliente.
        """

        connection = user["connection"]
        user["username"] = connection.recv(1024).decode()

        # Avisa que um novo usuário conectou-se ao servidor.
        self.__sendToAll(self.warningMessages["connected"].format(user["username"]))

        connection.settimeout(self.timeout)

        # Obtém as informações do cliente enquanto ele 
        # estiver online e o servidor rodando.
        while user["online"] and self.__running:

            try: 
                message = connection.recv(1024)
                if not message: break

            except socket.timeout: 
                continue

            except: 
                break

            # Repassa as informações para todos os clientes.
            self.__sendToAll(user["username"] + " : " + message.decode(), author = user)

        # Encerra a conexão com o usuário e informa para os outros clientes que ele saiu.
        if self.__running: self.__removeUser(user)
        self.__sendToAll(self.warningMessages["disconnected"].format(user["username"]), author = user)


    def __removeUser(self, user):

        """
        Encerra a conexão de um único usuário.
        """

        user["connection"].close()
        user["online"] = False
        self.__connections.remove(user)


    def __sendToAll(self, message, author = None):

        """
        Envia uma mensagem para todos os clientes, 
        exceto para o autor da mensagem.
        """

        self.messageCallback(message)

        for user in self.__connections:

            if not user is author:
                try: 
                    user["connection"].send((message + self.separator).encode())
                except: 
                    user["online"] = False


    def close(self) -> None:

        """
        Desliga o servidor, encerrando todas 
        as conexões dos clientes com ele.
        """

        self.__running = False

        for user in self.__connections:
            self.__removeUser(user)

        self.socket.close()


    def run(self, messageCallback) -> None:

        """
        Inicia o servidor para receber e repassar 
        as mensagens enviadas pelos clientes.
        """

        self.__running = True
        self.messageCallback = messageCallback
        Thread(target = self.__acceptConnections).start()


    def send(self, message: str) -> None:

        """
        Envia mensagem do servidor para os outros clientes.
        """

        if message and not message.isspace():
            self.__sendToAll(self.username + " : " + message)



