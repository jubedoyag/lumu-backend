import json
from kafka import KafkaConsumer
from app.services.service import IP_ADDRESSES

def kafka_consumer(topic, server):
    consumer = KafkaConsumer(topic, bootstrap_servers=server)
    for msg in consumer:

        msg_data = json.loads(msg.value.decode())

        timestamp = msg_data.get("timestamp")
        device_ip = msg_data.get("device_ip")

        IP_ADDRESSES.add(device_ip)
