from ensurepip import bootstrap
from kafka import KafkaConsumer, KafkaProducer
from json import loads, load, dumps
from time import sleep

# Simple consumer for all triggered events

consumer = KafkaConsumer(
    'task.trigger',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id=None,
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

def start():
    """Simple consumer to check that triggered events are being sent on
    the right topic
    """
    print("=== triggers_consumer ===", "STARTING UP")
    for event in consumer:
        print("=== triggers_consumer ===", event.value)
        sleep(0.5)

if __name__ == "__main__":
    start()
