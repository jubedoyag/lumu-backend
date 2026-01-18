from fastapi import APIRouter
from app.services.service import get_device_ip_count
from app.services.service import get_status

router = APIRouter()

@router.get("/number-ips")
async def get_number_unique_ips():
    return get_device_ip_count()

@router.get("/is-node-active")
def get_node_status():
    return get_status()

