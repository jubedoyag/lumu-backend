import urllib.request
import json
import time
import ipaddress
from app.core.config import logger, DISCOVERING_INTERVAL, NODES_NETWORK


DISCOVERED_NODES = {}


def get_response_data(url):
    try:
        with urllib.request.urlopen(url, timeout=0.01) as resp:
            data = resp.read().decode()
    except:
        return None

    return json.loads(data)


def discover_nodes():
    while True:
        for ip_address in list(ipaddress.ip_network(NODES_NETWORK).hosts()):
            response_data = get_response_data(f"http://{ip_address}:8000/is-node-active")
            if response_data is None:
                continue

            status = response_data.get("status")
            node_id = response_data.get("node_id")
            ip = str(ip_address)

            if status and node_id not in DISCOVERED_NODES:
                DISCOVERED_NODES[node_id] = ip
                logger.warning(f"Node discovered: {ip} - {node_id}")

        time.sleep(int(DISCOVERING_INTERVAL))

