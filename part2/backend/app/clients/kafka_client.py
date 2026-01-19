import json
from kafka import KafkaConsumer
from app.services.service import IP_ADDRESSES
from app.utils.validations import parse_date_to_utc
from app.utils.validations import is_ipv4_valid
from app.core.config import logger, KAFKA_SERVER, KAFKA_TOPIC


def kafka_consumer():
    consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_SERVER)
    for msg in consumer:

        msg_data = json.loads(msg.value.decode())

        timestamp = msg_data.get("timestamp")
        device_ip = msg_data.get("device_ip")

        try:

            parsed_timestamp = parse_date_to_utc(timestamp)
            if not is_ipv4_valid(device_ip):
                raise AssertionError("Device IP has invalid format")

            IP_ADDRESSES.add(device_ip)

        except Exception as e:
            logger.warning("Event ignored. Message validation error: {e}")

