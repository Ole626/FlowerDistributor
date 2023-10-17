import json
from pathlib import Path

from display_gui import DisplayGui
from control_gui import ControlGui


ROOT_DIR = Path(__file__).parent.parent
CONFIG_FILE_PATH = ROOT_DIR.joinpath('conf.json')


def main():
    client_type, id_value, font_size, broker_ip, broker_port = load_json_config(CONFIG_FILE_PATH)

    if client_type == 'Display':
        topics = ['client-' + id_value + '/label', 'client-' + id_value + '/id_test']
        gui = DisplayGui(broker_ip, broker_port, topics, id_value, font_size=font_size)
        gui.main()
    elif client_type == 'Control':
        gui = ControlGui(broker_ip, broker_port, 'control', int(id_value))
        gui.main()


def load_json_config(file_name):
    with open(file_name) as f:
        data = json.load(f)

    return data['client_type'], data['id_info'], data['font_size'], data['broker_ip'], data['broker_port']


if __name__ == '__main__':
    main()
