import logging
import os
from dotenv import load_dotenv

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

NODES_NETWORK = os.getenv("NODES_NETWORK")
DISCOVERING_INTERVAL = os.getenv("DISCOVERING_INTERVAL")
KAFKA_SERVER = os.getenv("KAFKA_SERVER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

