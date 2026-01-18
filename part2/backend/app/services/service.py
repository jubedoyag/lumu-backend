IP_ADDRESSES = set()

def get_status():
    return {"status": True}

def get_device_ip_count():
    return {"counting": len(IP_ADDRESSES)}
