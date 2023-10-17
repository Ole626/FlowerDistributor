import PySimpleGUI as sg
import time

from display_client import DisplayClient


class DisplayGui:

    def __init__(self, broker_ip, broker_port, topics, id_value, font_size=150, theme="DefaultNoMoreNagging"):
        self.broker_ip = broker_ip
        self.broker_port = broker_port
        self.topics = topics
        self.id_value = id_value
        self.theme = theme
        self.window = None
        self.font_size = font_size
        self.label = id_value

    def display_page(self):
        # Set class theme.
        sg.theme(self.theme)
        sg.set_options(element_padding=(0, 0))

        layout = [
            [sg.Text("", key="_FILLER_1_TEXT_", expand_x=True, expand_y=True, background_color="white")],
            [sg.Text(self.label, key="_DISPLAY_TEXT_", font=("Arial", self.font_size), auto_size_text=True, expand_x=True, background_color="white")],
            [sg.Text("", key="_FILLER_2_TEXT_", expand_x=True, expand_y=True, background_color="white")]
        ]

        self.window = sg.Window("Display Page", layout=layout, text_justification='c', no_titlebar=True, finalize=True, background_color="white", size=sg.Window.get_screen_size())

        self.window.maximize()

        display_client = DisplayClient(self.broker_ip, self.broker_port, self.id_value, self.topics, self)
        display_client.connect_broker()

        while True:
            event, values = self.window.read()

            if event == "_TEXT_UPDATE_":
                self.window["_DISPLAY_TEXT_"].update(values["_TEXT_UPDATE_"])
            if event in (sg.WINDOW_CLOSED, "Exit"):
                display_client.disconnect_broker()
                break

    def update_text(self, text):
        # Check if there is a window to update.
        if self.window is not None:
            # Raise an event from code to update the text.
            self.label = text
            self.window.write_event_value("_TEXT_UPDATE_", text)

    def show_mqtt_id(self, id_value):
        # Check if there is a window to update.
        if self.window is not None:
            self.window["_DISPLAY_TEXT_"].update(id_value, background_color="green")
            self.window["_FILLER_1_TEXT_"].update(background_color="green")
            self.window["_FILLER_2_TEXT_"].update(background_color="green")
            self.window.refresh()

    def hide_mqtt_id(self):
        # Check if there is a window to update.
        if self.window is not None:
            self.window["_DISPLAY_TEXT_"].update(self.label, background_color="white")
            self.window["_FILLER_1_TEXT_"].update(background_color="white")
            self.window["_FILLER_2_TEXT_"].update(background_color="white")
            self.window.refresh()

    def main(self):
        self.display_page()
