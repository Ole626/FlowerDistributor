from abstract_client import AbstractClient


class DisplayClient(AbstractClient):

    def __init__(self, broker, port, id, topic, text_element):
        super().__init__(broker, port, id)
        self.topic = topic
        self.text_element = text_element

    def connect_broker(self):
        super().connect_broker()
        self.subscribe(self.topic)

    def publish(self, topic, msg):
        pass

    def subscribe(self, topic):
        self.client.subscribe(topic)
        self.client.on_message = self.__on_message
        print(f"Subscribed to {topic}")

    def __on_message(self, client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        self.latest_msg = msg.payload.decode()