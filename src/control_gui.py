import PySimpleGUI as sg

from control_client import ControlClient


class ControlGui:

    def __init__(self, broker_ip, broker_port, id_value, screen_amount, theme="DefaultNoMoreNagging"):
        self.broker_ip = broker_ip
        self.broker_port = broker_port
        self.id_value = id_value
        self.screen_amount = screen_amount
        self.selected_screen = '1'
        self.theme = theme
        self.window = None
        self.test_ids_enabled = False

        self.last_sent_messages = {} # The key is the topic, the value is the message

    def control_page(self):
        sg.theme(self.theme)

        layout = [
            self.screen_frames(self.screen_amount),
            [sg.Push(),
             sg.Frame(layout=[
                [sg.InputText('', key='_INPUT_TEXT_', font=('Arial', 42))],
                [sg.Push(),
                 sg.Button("Update", key='_UPDATE_', font=("Arial", 28), enable_events=True),
                 sg.Push(),
                 sg.Button("Refresh", key='_REFRESH_', font=("Arial", 28), enable_events=True),
                 sg.Push() # Removed for complicated purposes
                 ]
             ], title="Scherm Update", font=('Arial', 32)),
             sg.Push()]
        ]

        self.window = sg.Window("Control Page", layout=layout, no_titlebar=False, finalize=True, size=(1920, 1080))

        #self.window.maximize()
        self.window.bind("<Escape>", "_ESCAPE_")

        cc = ControlClient(self.broker_ip, self.broker_port, self.id_value)
        cc.connect_broker()

        while True:
            event, values = self.window.read()

            if '_SELECT_' in event:
                self.select_screen(self.window, event.split('_')[2])

            elif event == '_UPDATE_':
                topic = 'client-' + self.selected_screen + '/label'
                text = values['_INPUT_TEXT_']

                # Save the last sent message
                key = int(self.selected_screen)
                self.last_sent_messages[key] = text

                # Publish the message and update the screen
                cc.publish(topic, text)
                self.window['_SCREEN_' + self.selected_screen + '_TEXT_'].update(text)

            elif event == '_REFRESH_':
                for key, value in self.last_sent_messages.items():
                    topic = 'client-' + str(key) + '/label'
                    cc.publish(topic, value)
                    self.window['_SCREEN_' + str(key) + '_TEXT_'].update(value)

            elif event in (sg.WINDOW_CLOSED, "Exit", "_ESCAPE_"):
                cc.disconnect_broker()
                break

            else:
                break

    def select_screen(self, window, screen_id):
        window['_SCREEN_' + self.selected_screen + '_TEXT_'].update(background_color='white')
        window['_SCREEN_' + screen_id + '_TEXT_'].update(background_color='light green')

        self.selected_screen = screen_id
        window.refresh()

    def screen_frames(self, amount):
        result = []

        for i in range(1, amount+1):
            result.append(sg.Frame(layout=[[sg.Text(str(i),
                                                    font=('Arial', 50),
                                                    key='_SCREEN_' + str(i) + '_TEXT_',
                                                    justification='c',
                                                    expand_x=True,
                                                    background_color='white')],
                                           [sg.Push(),
                                            sg.Button('Selecteer', font=('Arial', 28), key='_SCREEN_' + str(i) + '_SELECT_'),
                                            sg.Push()]],
                                   title='Scherm ' + str(i), expand_x=True, key='_SCREEN_' + str(i) + '_FRAME_', font=('Arial', 32)))

        return result

    def test_ids(self, control_broker, status):
        for i in range(1, self.screen_amount):
            topic = 'client-' + str(i) + '/id_test'
            text = status
            control_broker.publish(topic, text)

    def main(self):
        self.control_page()
