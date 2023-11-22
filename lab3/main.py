from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import ScreenManager
from os.path import join

# from kivy.core.window import Window
# Window.size = (412, 915)


HOLIDAYS = [
    {
        "name": "Новый Год",
        "date": "1 января",
        "description": "Празднование начала нового года.",
        "image": "new_year.png",
    },
    {
        "name": "Международный женский день",
        "date": "8 марта",
        "description": "Праздник весны и женской красоты.",
        "image": "8_march.png",
    },
    {
        "name": "День Победы",
        "date": "9 мая",
        "description": "Праздник победы в Великой Отечественной войне.",
        "image": "victory_day.png",
    },
    {
        "name": "День России",
        "date": "12 июня",
        "description": "Государственный праздник, посвященный Российской Федерации.",
        "image": "day_russia.png",
    },
    {
        "name": "День народного единства",
        "date": "4 ноября",
        "description": "Праздник, посвященный событиям, способствовавшим объединению России.",
        "image": "day_nation.png",
    },
    {
        "name": "День Защитника Отечества",
        "date": "23 февраля",
        "description": "Праздник, посвященный мужеству и защите родной земли.",
        "image": "23_february.png",
    },
    {
        "name": "Пасха",
        "date": "весна",
        "description": "Христианский праздник Воскресения Христова.",
        "image": "easter.png",
    },
    {
        "name": "День Космонавтики",
        "date": "12 апреля",
        "description": "Праздник посвященный первому полету человека в космос.",
        "image": "space.png",
    },
    {
        "name": "День Семьи, Любви и Верности",
        "date": "8 июля",
        "description": "Праздник, посвященный семейным ценностям и любви.",
        "image": "day_family.png",
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
            holiday_item.height = "100sp"
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
        self.ids.image_holiday.source = join("images", holiday["image"])
        self.ids.title_label.text = f"[b]Имя:[/b] {holiday['name']}"
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
        self.show_image = True
        Builder.load_file("main.kv")
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Light"
        self.active_holiday = HOLIDAYS[0]
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main_screen"))
        sm.add_widget(DetailScreen(name="detail_screen"))
        sm.add_widget(SettingsScreen(name="settings_screen"))
        self.sm = sm
        return sm

    def switch_theme(self, value):
        self.theme_cls.theme_style = "Dark" if value else "Light"
        self.theme_cls.primary_palette = "Blue" if value else "Orange"

    def switch_image(self, value):
        self.show_image = value
        detail_screen = self.sm.get_screen("detail_screen")
        detail_screen.ids.image_holiday.opacity = 1 if value else 0
        detail_screen.ids.image_holiday.size_hint = (1, 1) if value else (None, None)
        detail_screen.ids.image_holiday.reload()


HolidayApp().run()
