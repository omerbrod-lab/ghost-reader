from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
import json
import os
from datetime import datetime

DATA_FILE = "messages.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=2)
        header = BoxLayout(size_hint_y=None, height=60, padding=10)
        title = Label(
            text='Ghost Reader',
            font_size=24,
            bold=True,
            color=(0.07, 0.73, 0.4, 1)
        )
        header.add_widget(title)
        self.layout.add_widget(header)
        self.scroll = ScrollView()
        self.groups_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=1
        )
        self.groups_layout.bind(
            minimum_height=self.groups_layout.setter('height')
        )
        self.scroll.add_widget(self.groups_layout)
        self.layout.add_widget(self.scroll)
        self.add_widget(self.layout)

    def refresh_groups(self, data):
        self.groups_layout.clear_widgets()
        if not data:
            empty = Label(
                text='No messages yet...',
                halign='center',
                font_size=16,
                color=(0.5, 0.5, 0.5, 1)
            )
            self.groups_layout.add_widget(empty)
            return
        sorted_groups = sorted(
            data.items(),
            key=lambda x: x[1][-1]['timestamp'] if x[1] else 0,
            reverse=True
        )
        for group_name, messages in sorted_groups:
            last_msg = messages[-1]
            unread = sum(1 for m in messages if not m.get('read'))
            btn = Button(
                size_hint_y=None,
                height=75,
                background_color=(0.1, 0.1, 0.1, 1),
                background_normal=''
            )
            row = BoxLayout(padding=10, spacing=10)
            avatar = Label(
                text=group_name[0],
                size_hint_x=None,
                width=50,
                font_size=22,
                bold=True,
                color=(0.07, 0.73, 0.4, 1)
            )
            row.add_widget(avatar)
            info = BoxLayout(orientation='vertical')
            name_row = BoxLayout()
            name_lbl = Label(
                text=group_name,
                font_size=16,
                bold=True,
                color=(1, 1, 1, 1)
            )
            time_lbl = Label(
                text=last_msg.get('time', ''),
                font_size=12,
                size_hint_x=None,
                width=60,
                color=(0.6, 0.6, 0.6, 1)
            )
            name_row.add_widget(name_lbl)
            name_row.add_widget(time_lbl)
            preview_text = last_msg.get('sender', '') + ': ' + last_msg.get('text', '')
            preview = Label(
                text=preview_text,
                font_size=13,
                halign='right',
                color=(0.6, 0.6, 0.6, 1),
                text_size=(300, None)
            )
            info.add_widget(name_row)
            info.add_widget(preview)
            row.add_widget(info)
            if unread > 0:
                badge = Label(
                    text=str(unread),
                    size_hint_x=None,
                    width=30,
                    color=(0.07, 0.73, 0.4, 1),
                    bold=True
                )
                row.add_widget(badge)
            btn.add_widget(row)
            btn.bind(on_press=self.make_open_group(group_name))
            self.groups_layout.add_widget(btn)

    def make_open_group(self, group_name):
        def open_group(instance):
            app = App.get_running_app()
            app.current_group = group_name
            app.root.current = 'chat'
        return open_group

class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        header = BoxLayout(size_hint_y=None, height=60, padding=10, spacing=10)
        back_btn = Button(
            text='Back',
            size_hint_x=None,
            width=60,
            background_color=(0, 0, 0, 0)
        )
        back_btn.bind(on_press=self.go_back)
        self.group_title = Label(
            text='',
            font_size=18,
            bold=True,
            color=(1, 1, 1, 1)
        )
        header.add_widget(back_btn)
        header.add_widget(self.group_title)
        self.layout.add_widget(header)
        self.scroll = ScrollView()
        self.messages_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=4,
            padding=10
        )
        self.messages_layout.bind(
            minimum_height=self.messages_layout.setter('height')
        )
        self.scroll.add_widget(self.messages_layout)
        self.layout.add_widget(self.scroll)
        self.add_widget(self.layout)

    def load_messages(self, group_name, messages):
        self.group_title.text = group_name
        self.messages_layout.clear_widgets()
        for msg in messages:
            bubble = BoxLayout(size_hint_y=None, height=60, padding=8)
            msg_text = msg.get('sender', '') + '\n' + msg.get('text', '') + '\n' + msg.get('time', '')
            lbl = Label(
                text=msg_text,
                halign='right',
                valign='top',
                text_size=(300, None),
                color=(1, 1, 1, 1),
                font_size=14
            )
            bubble.add_widget(lbl)
            self.messages_layout.add_widget(bubble)
        app = App.get_running_app()
        for msg in messages:
            msg['read'] = True
        save_data(app.data)
        Clock.schedule_once(lambda dt: self.scroll_bottom(), 0.2)

    def scroll_bottom(self):
        self.scroll.scroll_y = 0

    def go_back(self, instance):
        App.get_running_app().root.current = 'main'

class GhostReaderApp(App):
    def __init__(self, **kwargs):
        super(GhostReaderApp, self).__init__(**kwargs)
        self.data = load_data()
        self.current_group = None

    def build(self):
        from kivy.core.window import Window
        Window.clearcolor = (0.07, 0.07, 0.07, 1)
        sm = ScreenManager()
        self.main_screen = MainScreen(name='main')
        self.chat_screen = ChatScreen(name='chat')
        sm.add_widget(self.main_screen)
        sm.add_widget(self.chat_screen)
        sm.bind(current=self.on_screen_change)
        Clock.schedule_interval(self.refresh_ui, 2)
        return sm

    def on_screen_change(self, sm, screen_name):
        if screen_name == 'chat' and self.current_group:
            msgs = self.data.get(self.current_group, [])
            self.chat_screen.load_messages(self.current_group, msgs)

    def refresh_ui(self, dt):
        self.data = load_data()
        self.main_screen.refresh_groups(self.data)

if __name__ == '__main__':
    GhostReaderApp().run()
