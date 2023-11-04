from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class CalculatorApp(App):
    def build(self):
        layout = GridLayout(rows=2, spacing=10, size_hint=(1, 1))
        self.result = TextInput(
            padding=20,
            font_size="50sp",
            halign="left",
            multiline=False,
            size_hint=(1, 0.3),
        )
        layout.add_widget(self.result)

        layout_buttons = GridLayout(cols=4, spacing=10, size_hint=(1, 1))
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+'
        ]

        for button in buttons:
            btn = Button(
                text=button,
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                font_size="32sp",
                background_color="#7883FF",
            )
            btn.bind(on_press=self.on_button_press)
            layout_buttons.add_widget(btn)
        layout.add_widget(layout_buttons)
        return layout

    def on_button_press(self, instance):
        current = self.result.text

        if instance.text == "C":
            self.result.text = ""
        elif instance.text == "=":
            try:
                self.result.text = str(eval(current))
            except Exception as e:
                self.result.text = "Error"
        else:
            self.result.text += instance.text


if __name__ == "__main__":
    CalculatorApp().run()
