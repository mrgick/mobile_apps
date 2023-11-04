from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView

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


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        scroll_view = ScrollView()

        grid_layout = BoxLayout(orientation="vertical", spacing="10sp", size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter("height"))
        grid_layout.bind(size=self.adjust_buttons_text_size)

        for holiday in HOLIDAYS:
            holiday_button = Button(
                text=holiday["name"],
                size_hint_y=None,
                height="100sp",
                background_color="#7883FF",
                font_size="30sp",
                valign="center",
                halign="center",
            )
            holiday_button.bind(
                on_press=lambda instance, h=holiday: self.show_detail_holiday(h)
            )
            grid_layout.add_widget(holiday_button)

        scroll_view.add_widget(grid_layout)

        self.add_widget(scroll_view)

    def adjust_buttons_text_size(self, instance, value):
        for child in instance.children:
            if isinstance(child, Button):
                child.text_size = (instance.width - 20, None)

    def show_detail_holiday(self, holiday):
        app = App.get_running_app()
        app.active_holiday = holiday
        self.manager.transition.direction = "left"
        self.manager.current = "detail_screen"


class DetailScreen(Screen):
    def __init__(self, **kwargs):
        super(DetailScreen, self).__init__(**kwargs)
        self.current_holiday = HOLIDAYS[0]
        self.show_details()

    def on_pre_enter(self, *largs):
        app = App.get_running_app()
        if app.active_holiday != self.current_holiday:
            self.current_holiday = app.active_holiday
            self.show_details()

    def show_details(self):
        holiday = self.current_holiday
        grid_layout = BoxLayout(orientation="vertical", spacing="10sp")

        name_label = Label(
            text=f"[b]Имя:[/b] {holiday['name']}",
            markup=True,
            valign="center",
            halign="center",
            font_size="30sp",
        )
        date_label = Label(
            text=f"[b]Дата:[/b] {holiday['date']}",
            markup=True,
            valign="center",
            halign="center",
            font_size="26sp",
        )
        description_label = Label(
            text=f"[b]Описание:[/b] {holiday['description']}",
            markup=True,
            valign="center",
            halign="center",
            font_size="26sp",
        )

        grid_layout.bind(size=self.adjust_labels_text_size)

        grid_layout.add_widget(name_label)
        grid_layout.add_widget(date_label)
        grid_layout.add_widget(description_label)

        back_button = Button(
            text="Закрыть",
            size_hint_y=None,
            height="100sp",
            text_size=(None, None),
            halign="center",
            valign="center",
            background_color="#7883FF",
            font_size="30sp",
        )
        back_button.bind(on_press=self.show_holidays_list)
        grid_layout.add_widget(back_button)

        self.clear_widgets()
        self.add_widget(grid_layout)

    def adjust_labels_text_size(self, instance, value):
        for child in instance.children:
            if isinstance(child, Label):
                child.text_size = (instance.width - 20, None)

    def show_holidays_list(self, instance):
        self.manager.transition.direction = "right"
        self.manager.current = "main_screen"


class HolidayApp(App):
    def build(self):
        self.active_holiday = HOLIDAYS[0]
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main_screen"))
        sm.add_widget(DetailScreen(name="detail_screen"))
        return sm


if __name__ == "__main__":
    HolidayApp().run()
