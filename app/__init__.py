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
        messageBox = self.root.get_screen("messageBox")

        username = menu.ids.username.text
        ip , port = self.validateData(menu.ids.ip.text, menu.ids.port.text)

        if not all((ip, port)):
            if not ip: menu.ids.ip.text = "Invalid IP"
            if not port: menu.ids.port.text = "Invalid Port"
            return -1

        messageBox.ids.connection.text = "%s:%i" % (ip, port)

        try:
            if mode.lower() == "server":
                self.connection = Server((ip, port), username)
            else:
                self.connection = Client((ip, port), username)

            self.connection.run(messageBox.insertMessage)

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

        Confirm: Esse parâmetro recebe um título para realizar uma confirmação.
        """

        if confirm:
            Confirm(confirm, super().stop).open()
        else:
            self.closeConnection()
            super().stop()


    def validateData(self, ip, port) -> tuple:

        """
        Valida o endereço IP e o Port.
        """

        ip = ip.lower() if ip else "localhost"

        if ip != "localhost":
            if [n.isnumeric() for n in ip.split(".")].count(True) != 4:
                ip = None 
        try: 
            port = int(port)
        except: 
            port = None
        return ip, port


class Menu(Screen):

    """
    Tela de menu onde o usuário pode inserir as informações
    de conexão e escolher entre criar ou conectar-se a um servidor.
    """

    def closeByKeyBoard(self, window, key, *args):

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


    def on_pre_enter(self):

        Window.bind(on_request_close = self.confirm)
        Window.bind(on_keyboard = self.closeByKeyBoard)


    def on_pre_leave(self):

        Window.unbind(on_request_close = self.confirm)
        Window.unbind(on_keyboard = self.closeByKeyBoard)


class MessageBox(Screen):

    """
    Tela para receber ou enviar mensagens.
    """

    def closeByKeyBoard(self, window, key, *args):

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
        Window.bind(on_keyboard = self.closeByKeyBoard)


    def on_pre_leave(self):

        App.get_running_app().closeConnection()

        screen = App.get_running_app().root.get_screen("messageBox")
        screen.ids.box.clear_widgets()

        Window.unbind(on_request_close = self.confirm)
        Window.unbind(on_keyboard = self.closeByKeyBoard)



