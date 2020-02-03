from app.confirm import Confirm
from conn.client import Client
from conn.server import Server
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from pygame import mixer


class App(App):

    connection = None

    def build(self):
        
        mixer.init(buffer = 1024)
        return ScreenManager()


    def createConnection(self, mode):

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

        if self.connection:
            self.connection.close()


    def stop(self, confirm = ""):

        if confirm:
            Confirm(confirm, super().stop).open()
        else:
            self.closeConnection()
            super().stop()


    def validateData(self, ip, port):

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

    def closeByKeyBoard(self, window, key, *args):

        if key == 27: 
            return self.confirm()


    def confirm(self, *args, **kwargs):

        App.get_running_app().stop("Are you sure you want to leave ?")
        return True


    def on_pre_enter(self):

        Window.bind(on_request_close = self.confirm)
        Window.bind(on_keyboard = self.closeByKeyBoard)


    def on_pre_leave(self):

        Window.unbind(on_request_close = self.confirm)
        Window.unbind(on_keyboard = self.closeByKeyBoard)


class MessageBox(Screen):

    def closeByKeyBoard(self, window, key, *args):

        if key == 27: 
            App.get_running_app().root.current = "menu"
        return True


    def confirm(self, *args, **kwargs):

        App.get_running_app().stop("Are you sure you want to leave ?")
        return True


    def getMessage(self):

        screen = App.get_running_app().root.get_screen("messageBox")
        message = screen.ids.input.text
        screen.ids.input.text = ""
        return message


    def insertMessage(self, message):

        if message:
            screen = App.get_running_app().root.get_screen("messageBox")

            mixer.music.load("sounds/newMessage.mp3")
            mixer.music.play()

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


