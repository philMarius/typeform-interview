from time import sleep
from json import dumps
from kafka import KafkaProducer
from datetime import datetime, timezone
import uuid

from events import tasks_done_events

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

def start():
    """Pings a load of task.done events at the task.done topic"""
    print("--- task_done_emitter ---", "STARTING UP")
    for j in tasks_done_events:
        print("--- task_done_emitter ---", j)
        j["id"] = str(uuid.uuid4())
        # Get UTC time of event emission
        j["occurred_on"] = datetime.now(timezone.utc).timestamp() * 1000
        future = producer.send('task.done', value=j)
        # Wait for event to send before progressing onto next event
        result = future.get(timeout=10)
        print("--- task_done_emitter ---", result)
        sleep(0.5)

if __name__ == "__main__":
    start()
