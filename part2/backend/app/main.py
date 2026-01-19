import threading
from fastapi import FastAPI
from app.routers.routes import router
from app.clients.kafka_client import kafka_consumer
from app.clients.nodes_client import discover_nodes


kafka_t = threading.Thread(target=kafka_consumer, daemon=True)
discovering_t = threading.Thread(target=discover_nodes, daemon=True)

kafka_t.start()
discovering_t.start()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello world"}

app.include_router(router)

