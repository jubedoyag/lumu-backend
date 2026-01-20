import argparse
import json
import random
import time
from datetime import datetime, timezone

from kafka import KafkaProducer
from app.core.config import KAFKA_SERVER, KAFKA_TOPIC

TIMESTAMP_FORMATS = [
    '%Y-%m-%dT%H:%M:%S.%fZ',
    '%Y-%m-%dT%H:%M:%S.%f',
    '%Y-%m-%dT%H:%M:%S',
    '%Y-%m-%d %H:%M:%S.%f',
    '%Y-%m-%d %H:%M:%S',
    'unix_millis',
    'unix_seconds',
]


def generate_timestamp():
    fmt = random.choice(TIMESTAMP_FORMATS)
    now = datetime.now(timezone.utc)
    if fmt == 'unix_millis':
        return str(int(now.timestamp() * 1000))
    elif fmt == 'unix_seconds':
        return str(int(now.timestamp()))
    else:
        return now.strftime(fmt)


def generate_device_ip():
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))


def start_producer(num_devices, num_messages, pause_ms):

    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    device_ips = [generate_device_ip() for _ in range(num_devices)]

    for i in range(num_messages):
        message = {
            'timestamp': generate_timestamp(),
            'device_ip': random.choice(device_ips),
            'error_code': random.randint(0, 10)
        }
        producer.send(KAFKA_TOPIC, value=message)
        print(f"Sent message {i + 1}: {message}")
        time.sleep(pause_ms / 1000.0)

    producer.flush()
    producer.close()

