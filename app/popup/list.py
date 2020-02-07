from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import os


class List(Popup):

    def __init__(self, title: str, size = ["400dp", "500dp"]):

        path = os.path.split(__file__)[0]
        self.content = Builder.load_file(os.path.join(path, "list.kv"))
        super().__init__(title = title, content = self.content, size_hint = (None, None), size = size)


    def insertItem(self, items, font_size = "15dp", height = "30dp", **kwargs):

        """
        Insere itens na lista.

        Param item: Deve ser uma lista contendo um ou dois valores somente, exemplo: ["carro", "moto"].
        """

        align = ["left", "right"]

        box = BoxLayout(size_hint_y = None, height = height)

        for item in items[:2]:

            label = Label(
                text = item,
                font_size = font_size, 
                size_hint_y = None, 
                height = height, 
                halign = align[items.index(item)], 
                **kwargs
                )
            label.bind(size = label.setter('text_size'))  
            box.add_widget(label)

        self.content.ids.box.add_widget(box)