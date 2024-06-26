from abstract_client import AbstractClient


class DisplayClient(AbstractClient):

    def __init__(self, broker, port, screen_id, topic_id, topics, gui):
        super().__init__(broker, port, screen_id)
        self.topics = topics
        self.gui = gui
        self.topic_string = f'client-{topic_id}'

    def connect_broker(self):
        super().connect_broker()
        for topic in self.topics:
            self.subscribe(topic)

    def on_message(self, client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        self.latest_msg = msg.payload.decode()

        if msg.topic == self.topic_string + "/label":
            self.gui.update_text(self.latest_msg)
        elif msg.topic == self.topic_string + "/id_test":
            if self.latest_msg == '1':
                self.gui.show_mqtt_id(self.topic_string)
            if self.latest_msg == '0':
                self.gui.hide_mqtt_id()
