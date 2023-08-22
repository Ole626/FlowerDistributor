import threading
import time

from control_client import ControlClient
from display_client import DisplayClient


def main():
    thread1 = threading.Thread(target=DisplayClient.main)
    thread1.start()

    time.sleep(0.5)

    ControlClient.main()


if __name__ == "__main__":
    main()
