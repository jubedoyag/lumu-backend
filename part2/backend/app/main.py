import threading
from fastapi import FastAPI
from app.routers import routes
from app.clients.kafka_client import kafka_consumer


t = threading.Thread(
    target=kafka_consumer,
    args=('test-topic', '127.0.0.1:9092'),
    daemon=True,
)
t.start()
#kafka_consumer(1, 2)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello world"}

app.include_router(routes.router)

