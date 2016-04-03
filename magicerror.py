from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty


class MagicError:
    def __init__(self, error):
        box = BoxLayout(orientation='vertical', size_hint=(0.6, 0.6))
        butt = Button(text='OK')
        lab = Label(text=error)
        box.add_widget(lab)
        box.add_widget(butt)
        popup = Popup(content=box, title='', auto_dismiss=False)
        butt.bind(on_press=popup.dismiss)
        popup.open()


class MagicError1:
    def __init__(self, error):
        butt = Button(text='OK')
        # popup = Popup(content=butt, title=error, title_size='20sp', auto_dismiss=False)
        popup = Popup(title=error, size_hint=(0.6, 0.6), title_size='40',
                      content=butt, auto_dismiss=False)
        butt.bind(on_press=popup.dismiss)
        popup.open()
        print(error)
