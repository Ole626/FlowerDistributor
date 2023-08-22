from abstract_client import AbstractClient


class DisplayClient(AbstractClient):

    def publish(self, topic, msg):
        pass

    def subscribe(self, topic):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            self.latest_msg = msg.payload.decode()

        self.client.subscribe(topic)
        self.client.on_message = on_message
        print(f"Subscribed to {topic}")
