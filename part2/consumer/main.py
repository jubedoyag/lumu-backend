import json
import threading
import time
from kafka import KafkaConsumer


IP_ADDRESSES = set()


def kafka_consumer(topic, server):

    consumer = KafkaConsumer(topic, bootstrap_servers=server)

    for msg in consumer:

        msg_data = json.loads(msg.value.decode())

        timestamp = msg_data.get("timestamp")
        device_ip = msg_data.get("device_ip")

        IP_ADDRESSES.add(device_ip)


def wait_key_pressing():
    while True:
        input("Press enter to see the number of addresses seen")
        print("- Number of addresses seen:", len(IP_ADDRESSES))
        time.sleep(1)


def main():

    try:

        t1 = threading.Thread(
            target=kafka_consumer,
            args=('test-topic', '127.0.0.1:9092'),
            daemon=True
        )
        t2 = threading.Thread(target=wait_key_pressing, daemon=True)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

    except KeyboardInterrupt:
        print("\nExecution interrupted\n")
        exit(0)


if __name__ == "__main__":
    main()
