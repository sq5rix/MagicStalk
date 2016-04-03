from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class MagicErrorBig:
    def __init__(self, error):
        box = BoxLayout(orientation='vertical')
        butt = Button(text='OK')
        lab = Label(text=error)
        box.add_widget(lab)
        box.add_widget(butt)
        popup = Popup(content=box, auto_dismiss=False)
        butt.bind(on_press=popup.dismiss)
        popup.open()


class MagicError:
    def __init__(self, error):
        butt = Button(text='OK')
        popup = Popup(content=butt, title=error, auto_dismiss=False)
        butt.bind(on_press=popup.dismiss)
        popup.open()
