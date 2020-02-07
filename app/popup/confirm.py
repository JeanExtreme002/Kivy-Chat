from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import os


class Confirm(Popup):
    
    """
    Classe para criar um Popup de confirmação.
    """

    def __init__(self, title, function, buttonText = ["Yes", "No"]):

        """
        Title: Título do Popup
        Function: Função que será executada ao confirmar (é passado a instância de Popup na chamada)
        ButtonText: Texto dos botões de confirmação e negação
        """

        path = os.path.split(__file__)[0] 
        content = Builder.load_file(os.path.join(path, "confirm.kv"))

        super().__init__(
            content = content,
            title = title, 
            size = ("400dp", "250dp"),
            size_hint = (None, None)
            )

        content.ids.image.source = os.path.join("images", "warning.png")

        content.ids.button_yes.text = buttonText[0]
        content.ids.button_yes.on_release = lambda: function(popup = self)

        content.ids.button_no.text = buttonText[1]
        content.ids.button_no.on_release = self.dismiss