from abc import ABC, abstractmethod
from paho.mqtt import client as mqtt_client
from threading import Thread


class AbstractClient(ABC):

    def __init__(self, broker, port, id):
        self.broker = broker
        self.port = port
        self.id = f'client-{id}'
        self.client = None
        self.connected = False
        self.latest_msg = None

    @abstractmethod
    def subscribe(self, topic):
        pass

    @abstractmethod
    def publish(self, topic, msg):
        pass

    def connect_broker(self):
        client = mqtt_client.Client(self.id)
        # client.username_pw_set(username, password)
        client.on_connect = self.__on_connect
        client.on_disconnect = self.__on_disconnect
        client.connect(self.broker, self.port)
        self.client = client

        thread = Thread(target=client.loop_forever)
        thread.start()

    def __on_connect(self, clt, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print(f"{self.id} connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    def __on_disconnect(self, clt, userdata, rc):
        print(f"{self.id} disconnected!")

    def disconnect_broker(self):
        self.client.disconnect()
