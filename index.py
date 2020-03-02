#!/usr/bin/python
#_*_ coding: utf-8 _*_

from kivy.config import Config
Config.set('graphics', 'width', 800)
Config.set('graphics', 'height', 500)
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from psutil import virtual_memory, process_iter

class RootScreen(ScreenManager):
    def __init__(self, **kwargs):
        super(RootScreen, self).__init__(**kwargs)
        self.current = 'home'

class Home(Screen):
    def __init__(self, *args, **kwargs):
        super(Home, self).__init__(*args, **kwargs)
       

class Head(BoxLayout):
    def __init__(self, **kwargs):
        super(Head, self).__init__(**kwargs)


class RightBody(BoxLayout):
    def __init__(self, **kwargs):
        super(RightBody, self).__init__(**kwargs)
        Clock.schedule_once(self.set_title_of_column, 0)

        Clock.schedule_interval(self.show_process, 10)

    def set_title_of_column(self, dt):
        titles = ['Name', 'Pid', 'Memory', 'User']
        for title in titles:
                self.ids.head_table.add_widget(TopTableItem(text=title))

    def show_process(self, dt):

        self.ids.body_table.clear_widgets()

        for proc in process_iter():
            p = proc.as_dict(attrs=['name', 'pid', 'memory_percent', 'username'])

            body_table_item = BodyTableItem()
            body_table_item.ids.name.text = p['name']
            body_table_item.ids.pid.text = str(p['pid'])
            body_table_item.ids.memory.text = str(p['memory_percent'])
            body_table_item.ids.user.text = p['username']

            self.ids.body_table.add_widget(body_table_item)
    


class TopTableItem(Label):
    def __init__(self, **kwargs):
        super(TopTableItem, self).__init__(**kwargs)


class BodyTableItem(BoxLayout):
    def __init__(self, **kwargs):
        super(BodyTableItem, self).__init__(**kwargs)


class LeftBody(BoxLayout):
    def __init__(self, **kwargs):
        super(LeftBody, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_memory_infos, .5)
        Clock.schedule_once(self.set_type_info, 0)
   
    def update_memory_infos(self, dt):
        self.ids.info.clear_widgets()
        infos = self.get_memory_infos()
        for key in infos.keys(): 
            info = Label(text=str(infos[key]),
                         color=(.1, .9, .2, 1),
                         font_name='DejaVuSans',)
            self.ids.info.add_widget(info)
    
    def set_type_info(self, dt):
        infos = self.get_memory_infos()
        for key in infos.keys():
            tipo = Label(text=key,
                         font_name= 'DejaVuSans',
                         font_size= 14,
                         color= (1, 1, 1, 1))

            self.ids.tipo.add_widget(tipo)


    def get_memory_infos(self):

        memory = virtual_memory()
        output = {'Used': memory.used,
                  'Avaliable':memory.available,
                  'Total': memory.total,
                  'Inactive': memory.inactive,
                  'Active': memory.active,
                  'Cached': memory.cached,
                  'Free': memory.free,
                  'Percent': memory.percent,
                  'Slab': memory.slab,
                  'Shared': memory.shared,
              }

        return output


class Main(App):
    def build(self):
        return RootScreen()

if __name__ == '__main__':
    Main().run()
