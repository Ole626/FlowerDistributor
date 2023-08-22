import time

from control_client import ControlClient
from display_client import DisplayClient

BROKER_IP = "192.168.0.101"
BROKER_PORT = 1883
TOPIC = "python/test"


def main():
    cc = ControlClient(BROKER_IP, BROKER_PORT, "Control")
    dc = DisplayClient(BROKER_IP, BROKER_PORT, "Display")

    cc.connect_broker()
    dc.connect_broker()

    dc.subscribe(TOPIC)
    time.sleep(1)
    cc.publish(TOPIC, "Test Message")

    cc.disconnect_broker()

    while not dc.latest_msg:
        time.sleep(1)
        
    dc.disconnect_broker()



if __name__ == "__main__":
    main()
