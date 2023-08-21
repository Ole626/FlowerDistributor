from abstract_client import AbstractClient


class ControlClient(AbstractClient):

    def publish(self, topic):
        msg = "This is a test message."
        result = self.client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Sent `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

    def subscribe(self, topic):
        pass
