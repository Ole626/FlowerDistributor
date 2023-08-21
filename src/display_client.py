from abstract_client import AbstractClient


class DisplayClient(AbstractClient):

    def publish(self, topic):
        pass

    def subscribe(self, topic):
        if self.connected:
            def on_message(client, userdata, msg):
                print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

            self.client.subscribe(topic)
            self.client.on_message = on_message
            print(f"Subscribed to {topic}")
        else:
            print("Failed to subscribe: not connected.")
