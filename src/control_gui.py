import PySimpleGUI as sg

from display_client import DisplayClient
from control_client import ControlClient

BROKER_IP = "192.168.0.101"
BROKER_PORT = 1883


class ControlGui:

    def __init__(self, theme="DefaultNoMoreNagging"):
        self.theme = theme

    def control_page(self, topics):
        sg.theme(self.theme)

        layout = [
            [sg.Text("Test", background_color="black", text_color="white", font=("Arial", 10), size=(10, 5), justification="center")]
        ]

        window = sg.Window("Control Page", layout, size=(300, 300))

        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED:
                break

    def start_page(self):
        sg.theme(self.theme)

        cc = ControlClient(BROKER_IP, BROKER_PORT, "Control")

        cc.connect_broker()

        layout = [
            [sg.Frame("Publisher", [
                [sg.Text(cc.screen_id, size=(15,1)),
                 sg.InputText(tooltip="Enter your message here", key="msg", size=(20, 1)),
                 sg.Button("Publish", enable_events=True)],
                [sg.Button("Test ID On", enable_events=True),
                 sg.Button("Test ID Off", enable_events=True)]
            ])],
            [sg.Exit()]
        ]

        window = sg.Window("Test Page", layout)

        while True:
            event, values = window.read()

            if event == "Publish":
                cc.publish('client-1/label', values["msg"])
            if event == "Test ID On":
                cc.publish("client-1/id_test", 1)
            if event == "Test ID Off":
                cc.publish("client-1/id_test", 0)
            if event == "Exit" or event == sg.WINDOW_CLOSED:
                cc.disconnect_broker()
                break

    @staticmethod
    def main():
        gui = ControlGui()
        gui.start_page()
        #gui.control_page(["topic1", "topic2"])


if __name__ == "__main__":
    ControlGui.main()
