from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import ScreenManager

Window.size = (412, 915)


HOLIDAYS = [
    {
        "name": "Новый Год",
        "date": "1 января",
        "description": "Празднование начала нового года.",
    },
    {
        "name": "Международный женский день",
        "date": "8 марта",
        "description": "Праздник весны и женской красоты.",
    },
    {
        "name": "День Победы",
        "date": "9 мая",
        "description": "Праздник победы в Великой Отечественной войне.",
    },
    {
        "name": "День России",
        "date": "12 июня",
        "description": "Государственный праздник, посвященный Российской Федерации.",
    },
    {
        "name": "День народного единства",
        "date": "4 ноября",
        "description": "Праздник, посвященный событиям, способствовавшим объединению России.",
    },
    {
        "name": "День Защитника Отечества",
        "date": "23 февраля",
        "description": "Праздник, посвященный мужеству и защите родной земли.",
    },
    {
        "name": "Пасха",
        "date": "весна",
        "description": "Христианский праздник Воскресения Христова.",
    },
    {
        "name": "День Космонавтики",
        "date": "12 апреля",
        "description": "Праздник посвященный первому полету человека в космос.",
    },
    {
        "name": "День Семьи, Любви и Верности",
        "date": "8 июля",
        "description": "Праздник, посвященный семейным ценностям и любви.",
    },
]


class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        list_layout = self.ids.holiday_list

        for holiday in HOLIDAYS:
            holiday_item = TwoLineListItem(
                text=holiday["name"],
                secondary_text=holiday["date"],
            )
            holiday_item.bind(
                on_release=lambda instance, h=holiday: self.show_detail_holiday(h)
            )
            list_layout.add_widget(holiday_item)

    def show_settings(self):
        self.manager.transition.direction = "right"
        self.manager.current = "settings_screen"

    def show_detail_holiday(self, holiday):
        app = MDApp.get_running_app()
        app.active_holiday = holiday
        self.manager.transition.direction = "left"
        self.manager.current = "detail_screen"


class DetailScreen(MDScreen):
    def __init__(self, **kwargs):
        super(DetailScreen, self).__init__(**kwargs)
        self.current_holiday = HOLIDAYS[0]
        self.show_details()

    def on_pre_enter(self, *largs):
        app = MDApp.get_running_app()
        if app.active_holiday != self.current_holiday:
            self.current_holiday = app.active_holiday
            self.show_details()

    def show_details(self):
        holiday = self.current_holiday
        self.ids.name_label.text = f"[b]Имя:[/b] {holiday['name']}"
        self.ids.date_label.text = f"[b]Дата:[/b] {holiday['date']}"
        self.ids.description_label.text = f"[b]Описание:[/b] {holiday['description']}"

    def show_holidays_list(self, instance):
        self.manager.transition.direction = "right"
        self.manager.current = "main_screen"


class SettingsScreen(MDScreen):
    def show_holidays_list(self, instance):
        self.manager.transition.direction = "left"
        self.manager.current = "main_screen"


class HolidayApp(MDApp):
    def build(self):
        Builder.load_file("main.kv")
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Light"
        self.active_holiday = HOLIDAYS[0]
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main_screen"))
        sm.add_widget(DetailScreen(name="detail_screen"))
        sm.add_widget(SettingsScreen(name="settings_screen"))
        return sm

    def switch_theme(self, value):
        self.theme_cls.theme_style = "Dark" if value else "Light"
        self.theme_cls.primary_palette = "Blue" if value else "Orange"


HolidayApp().run()
