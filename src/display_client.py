from abstract_client import AbstractClient


BROKER_IP = "192.168.0.101"
BROKER_PORT = 1883
TOPIC = "python/test"


class DisplayClient(AbstractClient):

    def publish(self, topic):
        pass

    def subscribe(self, topic):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            client.disconnect()

        self.client.subscribe(topic)
        self.client.on_message = on_message
        print(f"Subscribed to {topic}")

    @staticmethod
    def main():
        dis_client = DisplayClient(BROKER_IP, BROKER_PORT, "display")

        dis_client.connect_broker()
        dis_client.subscribe(TOPIC)
        dis_client.client.loop_forever()
