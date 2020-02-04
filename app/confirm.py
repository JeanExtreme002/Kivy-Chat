from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
import os


class Confirm(Popup):
    
    """
    Classe para criar um Popup de confirmação.
    """

    def __init__(self, title, function, buttonText = ["Yes", "No"]):

        """
        Title: Título do Popup
        Function: Função que será executada ao confirmar
        ButtonText: Texto dos botões de confirmação e negação
        """

        content = BoxLayout(orientation = "vertical", padding = "10dp")

        super().__init__(
            content = content,
            title = title, 
            size = ("400dp", "250dp"),
            size_hint = (None, None)
            )

        image = Image(source = os.path.join("images","warning.png"))
        buttonBox = BoxLayout(spacing = 2)

        buttonBox.add_widget(
            Button(
                text = buttonText[0], font_size = "20dp",
                on_release = lambda button: function(), 
                size_hint_y = None, height = "50dp"
                )
            )
        buttonBox.add_widget(
            Button(
                text = buttonText[1], font_size = "20dp",
                on_release = self.dismiss, 
                size_hint_y = None, height = "50dp"
                )
            )

        content.add_widget(image)
        content.add_widget(buttonBox)