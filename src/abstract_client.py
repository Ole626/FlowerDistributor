from abc import ABC, abstractmethod
from paho.mqtt import client as mqtt_client
from threading import Thread


class AbstractClient(ABC):

    def __init__(self, broker, port, screen_id):
        self.broker = broker
        self.port = port
        self.screen_id = f'client-{screen_id}'
        self.client = None
        self.connected = False
        self.latest_msg = None

    @abstractmethod
    def on_message(self, client, userdata, msg):
        pass

    def subscribe(self, topic):
        self.client.subscribe(topic)
        self.client.on_message = self.on_message
        print(f"Subscribed to {topic}")

    def publish(self, topic, msg):
        result = self.client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Sent `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

    def connect_broker(self):
        client = mqtt_client.Client(self.screen_id)
        # client.username_pw_set(username, password)
        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        client.connect(self.broker, self.port)
        self.client = client

        thread = Thread(target=client.loop_forever)
        thread.start()

    def on_connect(self, clt, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print(f"{self.screen_id} connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_disconnect(self, clt, userdata, rc):
        print(f"{self.screen_id} disconnected!")

    def disconnect_broker(self):
        self.client.disconnect()
