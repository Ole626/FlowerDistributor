import PySimpleGUI as sg
import time

from display_client import DisplayClient


class DisplayGui:

    def __init__(self, broker_ip, broker_port, topics, client_id, topic_id, font_size=150, theme="DefaultNoMoreNagging"):
        self.broker_ip = broker_ip
        self.broker_port = broker_port
        self.topics = topics
        self.client_id = client_id
        self.topic_id = topic_id
        self.theme = theme
        self.window = None
        self.font_size = font_size
        self.label = topic_id

    def display_page(self):
        # Set class theme.
        sg.theme(self.theme)
        sg.set_options(element_padding=(0, 0))

        layout = [
            [sg.Text("", key="_FILLER_1_TEXT_", expand_x=True, expand_y=True, background_color="yellow")],
            [sg.Text(self.label, key="_DISPLAY_TEXT_", font=("Arial", self.font_size), auto_size_text=True, expand_x=True, background_color="yellow")],
            [sg.Text("", key="_FILLER_2_TEXT_", expand_x=True, expand_y=True, background_color="yellow")]
        ]

        self.window = sg.Window("Display Page", layout=layout, text_justification='c', no_titlebar=True, finalize=True, background_color="yellow", size=sg.Window.get_screen_size())

        self.window.maximize()
        self.window.bind("<Escape>", "_ESCAPE_")

        display_client = DisplayClient(self.broker_ip, self.broker_port, self.client_id, self.topic_id, self.topics, self)
        display_client.connect_broker()

        while True:
            event, values = self.window.read()

            if event == "_TEXT_UPDATE_":
                self.window["_DISPLAY_TEXT_"].update(values["_TEXT_UPDATE_"])
            elif event in (sg.WINDOW_CLOSED, "Exit", "_ESCAPE_"):
                display_client.disconnect_broker()
                break
            else:
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
            self.window["_DISPLAY_TEXT_"].update(topic_id, background_color="white")
            self.window["_FILLER_1_TEXT_"].update(background_color="white")
            self.window["_FILLER_2_TEXT_"].update(background_color="white")
            self.window.refresh()

    def hide_mqtt_id(self):
        # Check if there is a window to update.
        if self.window is not None:
            self.window["_DISPLAY_TEXT_"].update(self.label, background_color="yellow")
            self.window["_FILLER_1_TEXT_"].update(background_color="yellow")
            self.window["_FILLER_2_TEXT_"].update(background_color="yellow")
            self.window.refresh()

    def main(self):
        self.display_page()
