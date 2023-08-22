import PySimpleGUI as sg

from display_client import DisplayClient
from control_client import ControlClient

BROKER_IP = "192.168.0.101"
BROKER_PORT = 1883
TOPIC = "python/test"


class GUI:

    def __init__(self, theme="DefaultNoMoreNagging"):
        self.theme = theme

    def start_page(self):
        sg.theme(self.theme)

        dc = DisplayClient(BROKER_IP, BROKER_PORT, "Display")
        cc = ControlClient(BROKER_IP, BROKER_PORT, "Control")

        dc.connect_broker()
        cc.connect_broker()

        layout = [
            [sg.Frame("Subscriber", [
                [sg.Text(dc.id, size=(15, 1)),
                 sg.Text(dc.latest_msg, key="msg_text", size=(30, 1)),
                 sg.Button("Refresh", enable_events=True),
                 sg.Button("Subscribe", enable_events=True)]
            ])],
            [sg.Frame("Publisher", [
                [sg.Text(cc.id, size=(15,1)),
                 sg.InputText(tooltip="Enter your message here", key="msg", size=(20, 1)),
                 sg.Button("Publish", enable_events=True)]
            ])],
            [sg.Exit()]
        ]

        window = sg.Window("Test Page", layout)

        while True:
            event, values = window.read()

            if event == "Subscribe":
                dc.subscribe(TOPIC)
            if event == "Refresh":
                window["msg_text"].update(dc.latest_msg)
            if event == "Publish":
                cc.publish(TOPIC, values["msg"])
            if event == "Exit" or event == sg.WINDOW_CLOSED:
                dc.disconnect_broker()
                cc.disconnect_broker()
                break

    @staticmethod
    def main():
        gui = GUI()

        gui.start_page()


if __name__ == "__main__":
    GUI.main()
