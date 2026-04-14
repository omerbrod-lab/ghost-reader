from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.utils import platform
import json
import os
from datetime import datetime

# --- שמירת נתונים ---
DATA_FILE = "messages.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --- מסך ראשי: רשימת קבוצות ---
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=2)

        # כותרת
        header = BoxLayout(size_hint_y=None, height=60,
                          padding=10)
        title = Label(text='👻 Ghost Reader',
                     font_size=24, bold=True,
                     color=(0.07, 0.73, 0.4, 1))
        header.add_widget(title)
        self.layout.add_widget(header)

        # רשימת קבוצות
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
