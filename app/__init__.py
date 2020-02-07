from app.popup.confirm import Confirm
from app.popup.list import List
from app.sound import SoundLoader
from conn.client import Client
from conn.server import Server
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
import os


class App(App):

    """
    Classe principal da aplicação.
    """

    connection = None


    def build(self):
        
        self.soundLoader = SoundLoader()
        return ScreenManager()


    def createConnection(self, mode: str) -> None:

        """
        Obtém as informações dos widgets TextInput
        e cria uma conexão (Server / Client).
        """

        menu = self.root.get_screen("menu")
        username, ip , port = menu.getInfo()

        if not all([username, ip, port]): 
            return -1

        # Mostra na caixa de mensagens o endereço do servidor atual.
        messageBox = self.root.get_screen("messageBox")
        messageBox.ids.connection.text = "%s:%i" % (ip, port)

        try:
            if mode.lower() == "server":
                self.connection = Server((ip, port), username)
            else:
                self.connection = Client((ip, port), username)

            self.connection.run(messageBox.insertMessage)

            # Apaga a mensagem de erro e vai para a caixa de mensagens.
            menu.ids.message.text = ""
            self.root.current = "messageBox"
            
        except:
            menu.ids.message.text = "Failed to connect."


    def closeConnection(self):

        """
        Encerra a conexão.
        """

        if self.connection:
            self.connection.close()


    def stop(self, confirm = "", popup = None):

        """
        Método para fechar o aplicativo.

        Param confirm: Esse parâmetro recebe um título para realizar 
        uma confirmação por uma janela pop-up.
        """

        if confirm:
            Confirm(confirm, self.stop).open()
        else:
            self.closeConnection()
            super().stop()


class Menu(Screen):

    """
    Tela de menu onde o usuário pode inserir as informações
    de conexão e escolher entre criar ou conectar-se a um servidor.
    """

    USERNAME_SIZE_LIMIT = 20


    def getInfo(self, validate = True):

        """
        Obtém os dados inseridos pelo usuário.
        """

        username = self.ids.username.text
        ip = self.ids.ip.text
        port = self.ids.port.text

        if validate:
            username = self.validate_username(username)
            ip = self.validate_ip(ip)
            port = self.validate_port(port)

        return username, ip, port


    def validate_ip(self, ip):

        """
        Valida o endereço IP.
        """

        ip = ip.lower() if ip else "localhost"

        if ip != "localhost":

            # Verifica se o endereço está no formato "xxx.xxx.xxx.xxx".
            if [n.isnumeric() for n in ip.split(".")].count(True) != 4:
                self.ids.ip.text = "Invalid IP"
                return None
        return ip 


    def validate_port(self, port):

        """
        Valida o port number.
        """

        try: 
            port = int(port)

            if not 1 <= port <= 65535:
                self.ids.port.text = "The port number must be 1 to 65535"
                port = None

        except ValueError:
            self.ids.port.text = "Invalid Port"
            port = None

        finally: return port


    def validate_username(self, username):

        """
        Valida o nome de usuário.
        """

        if username and not username.isspace():

            # Limita o tamanho do nome de usuário.
            if len(username) > self.USERNAME_SIZE_LIMIT:
                username = username[: self.USERNAME_SIZE_LIMIT + 1 - 3] + "..."
            return username

        else:
            self.ids.username.text = "Enter your username"
            return None


class MessageBox(Screen):

    """
    Tela para receber ou enviar mensagens.
    """

    def close(self):

        """
        Fecha o chat e volta para o menu.
        """

        def changeScreen(popup):

            popup.dismiss()
            App.get_running_app().root.current = "menu"

        Confirm("Are you sure you want to leave ?", changeScreen).open()
        return True


    def close_by_keyboard(self, window, key, *args):

        """
        Fecha o chat e volta para o menu através do botão de voltar.
        """

        if key == 27: 
            self.close()
        return True


    def getMessage(self) -> str:

        """
        Obtém mensagem do TextInput.
        """

        screen = App.get_running_app().root.get_screen("messageBox")
        message = screen.ids.input.text
        screen.ids.input.text = ""
        return message


    def insertMessage(self, message: str) -> None:

        """
        Adiciona para a caixa de mensagens uma nova mensagem.
        """

        if message:

            app = App.get_running_app()
            screen = app.root.get_screen("messageBox")

            app.soundLoader.play(os.path.join("sounds","newMessage.mp3"))

            label = Label(text = message, font_size = "15dp", size_hint_y = None, height = "30dp", halign = "left")
            label.bind(size = label.setter('text_size'))  
            screen.ids.box.add_widget(label)


    def showUsers(self):

        """
        Mostra uma lista com todos os usuários conectados (apenas no lado do servidor).
        """

        app = App.get_running_app()

        if isinstance(app.connection, Server):

            popup = List("Connected Users")

            for user in app.connection.users:

                address = "{}:{}".format(*user[0])
                username = user[1]

                popup.insertItem([username, address])
            popup.open()


    def stop(self, *args, **kwargs):

        """
        Fecha o aplicativo.
        """

        App.get_running_app().stop("Are you sure you want to leave ?")
        return True


    def on_pre_enter(self):

        Window.bind(on_request_close = self.stop)
        Window.bind(on_keyboard = self.close_by_keyboard)


    def on_pre_leave(self):

        App.get_running_app().closeConnection()

        # Remove todas as mensagens da sessão.
        screen = App.get_running_app().root.get_screen("messageBox")
        screen.ids.box.clear_widgets()

        Window.unbind(on_request_close = self.stop)
        Window.unbind(on_keyboard = self.close_by_keyboard)



