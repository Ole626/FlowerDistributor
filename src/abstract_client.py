from abc import ABC, abstractmethod
from paho.mqtt import client as mqtt_client


class AbstractClient(ABC):

    def __init__(self, broker, port, id):
        self.broker = broker
        self.port = port
        self.id = f'client-{id}'
        self.client = None
        self.connected = False

    @abstractmethod
    def subscribe(self, topic):
        pass

    @abstractmethod
    def publish(self, topic):
        pass

    def connect_broker(self):
        def on_connect(clt, userdata, flags, rc):
            if rc == 0:
                self.connected = True
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(self.id)
        # client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        self.client = client
