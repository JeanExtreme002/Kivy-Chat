from app.confirm import Confirm
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


    def stop(self, confirm = ""):

        """
        Método para fechar a aplicação.
        Param confirm: Esse parâmetro recebe um título para realizar uma confirmação.
        """

        if confirm:
            Confirm(confirm, super().stop).open()
        else:
            self.closeConnection()
            super().stop()


class Menu(Screen):

    """
    Tela de menu onde o usuário pode inserir as informações
    de conexão e escolher entre criar ou conectar-se a um servidor.
    """

    def close_by_keyboard(self, window, key, *args):

        """
        Fecha a aplicação através do botão de voltar.
        """

        if key == 27: 
            return self.confirm()


    def confirm(self, *args, **kwargs):

        """
        Confirma se o usuário deseja sair.
        """

        App.get_running_app().stop("Are you sure you want to leave ?")
        return True


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


    def on_pre_enter(self):

        Window.bind(on_request_close = self.confirm)
        Window.bind(on_keyboard = self.close_by_keyboard)


    def on_pre_leave(self):

        Window.unbind(on_request_close = self.confirm)
        Window.unbind(on_keyboard = self.close_by_keyboard)


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
            return username
        else:
            self.ids.username.text = "Enter your username"
            return None


class MessageBox(Screen):

    """
    Tela para receber ou enviar mensagens.
    """

    def close_by_keyboard(self, window, key, *args):

        """
        Vai para o menu através do botão de voltar.
        """

        if key == 27: 
            App.get_running_app().root.current = "menu"
        return True


    def confirm(self, *args, **kwargs):

        """
        Confirma se o usuário deseja sair.
        """

        App.get_running_app().stop("Are you sure you want to leave ?")
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


    def on_pre_enter(self):

        Window.bind(on_request_close = self.confirm)
        Window.bind(on_keyboard = self.close_by_keyboard)


    def on_pre_leave(self):

        App.get_running_app().closeConnection()

        # Remove todas as mensagens da sessão.
        screen = App.get_running_app().root.get_screen("messageBox")
        screen.ids.box.clear_widgets()

        Window.unbind(on_request_close = self.confirm)
        Window.unbind(on_keyboard = self.close_by_keyboard)



