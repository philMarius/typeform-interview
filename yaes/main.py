import threading
from kafka.errors import NoBrokersAvailable

import task_done_emitter
import yaes
import triggers_consumer

if __name__ == "__main__":
    task_done_emitter_thread = threading.Thread(target=task_done_emitter.start)
    yaes_thread = threading.Thread(target=yaes.start)
    triggers_consumer_thread = threading.Thread(target=triggers_consumer.start)

    task_done_emitter_thread.start()
    triggers_consumer_thread.start()
    yaes.start()
