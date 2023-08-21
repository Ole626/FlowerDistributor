from control_client import ControlClient
from display_client import DisplayClient


BROKER_IP = "192.168.0.101"
BROKER_PORT = 1883
TOPIC = "python/test"

def main():
    ctrl_client = ControlClient(BROKER_IP, BROKER_PORT, 1)
    dis_client = DisplayClient(BROKER_IP, BROKER_PORT, 2)

    ctrl_client.connect_broker()
    dis_client.connect_broker()

    dis_client.subscribe(TOPIC)
    ctrl_client.publish(TOPIC)


if __name__ == "__main__":
    main()
