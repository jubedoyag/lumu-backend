import threading
from fastapi import FastAPI
from app.services.kafka_producer import start_producer


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "hola mundo"}

@app.get("/start")
def start_kafka_producer(num_devices:int=100, num_messages:int=1000, pause_ms:int=100):
    t = threading.Thread(
        target=start_producer,
        args=(num_devices, num_messages, pause_ms)
    )
    t.start()
    return {"started": True}

