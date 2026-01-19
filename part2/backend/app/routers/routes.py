from fastapi import APIRouter
from app.services.service import get_local_ip_count
from app.services.service import get_global_ip_count
from app.services.service import get_status

router = APIRouter()

@router.get("/is-node-active")
def get_node_status():
    return get_status()

@router.get("/number-ips")
def get_number_unique_ips():
    return get_local_ip_count()

@router.get("/global-number-ips")
async def get_global_number_ips():
    return await get_global_ip_count()

