from abstract_client import AbstractClient


BROKER_IP = "192.168.0.101"
BROKER_PORT = 1883
TOPIC = "python/test"


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

    @staticmethod
    def main():
        ctrl_client = ControlClient(BROKER_IP, BROKER_PORT, "control")

        ctrl_client.connect_broker()

        ctrl_client.client.loop_start()
        ctrl_client.publish(TOPIC)
        ctrl_client.client.disconnect()
        ctrl_client.client.loop_stop()
