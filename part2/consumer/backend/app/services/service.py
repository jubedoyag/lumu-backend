import httpx
import uuid
from app.core.config import logger
from app.clients.nodes_client import DISCOVERED_NODES


IP_ADDRESSES = set()
NODE_ID = uuid.uuid4()


def get_status():
    return {"status": True, "node_id": NODE_ID}

def get_local_ip_count():
    return {"counting": len(IP_ADDRESSES)}

async def get_global_ip_count():
    votes = {}

    counting = len(IP_ADDRESSES)
    voting_nodes = 0

    for node_id in DISCOVERED_NODES:
        node = DISCOVERED_NODES.get(node_id)

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"http://{node}:8000/number-ips")
            response_data = response.json()
        except Exception as e:
            logger.warning(f"Error while trying to connect to '{node}:8000': {e}")
            continue

        voting_nodes += 1

        counting = response_data.get("counting")
        votes[counting] = votes[counting]+1 if votes.get(counting) else 1

    max_count = counting
    for count in votes:
        if votes.get(max_count) and votes.get(count) > votes.get(max_count):
            max_count = count

    return {
        "number": max_count,
        "voted_by": votes.get(max_count),
        "voting_nodes": voting_nodes,
        "votes": votes,
    }

