from kafka import KafkaConsumer, KafkaProducer
from json import loads, load, dumps
from time import sleep
from datetime import datetime, timezone


consumer = KafkaConsumer(
    'task.done',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id=None,
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

def emit_triggered_event(event, trigger):
    """Emit triggered event to task.trigger with new payload of trigger name"""
    emitted_event = event
    event["payload"] = {
        "trigger_rule": trigger
    }
    event["occurred_on"] = datetime.now(timezone.utc).timestamp() * 1000
    future = producer.send('task.trigger', value=emitted_event)
    result = future.get(timeout=10)

    return result

def fetch_rules(rule_json="./trigger_rules.json"):
    """Fetch rules for processing.

    Returns a dict of task_name: trigger_rule and validates that the rules
    are added correctly. Validation is checking whether duplicate rules exist
    """
    with open(rule_json) as f:
        trigger_rules_file = load(f)

    trigger_rule_names = [x["trigger_rule"] for x in trigger_rules_file["include"]]
    if len(set(trigger_rule_names)) != len(trigger_rule_names):
        raise Exception("Trigger rule names are not unique! Check to see if duplicate rules exist in config file")

    trigger_dict = {x["task_name"]: x["trigger_rule"] for x in trigger_rules_file["include"]}
    return trigger_dict

def start():
    """Listens to task.done topic, pings matching events in triggers json to
    task.trigger topic
    """
    print("+++ yaes +++", "STARTING UP")
    triggers = fetch_rules()

    for event in consumer:
        event_data = event.value
        print("+++ yaes +++", event_data)

        task_name = event_data["payload"]["task_name"]
        if task_name in triggers.keys():
            triggered_rule = triggers[task_name]
            print("+++ yaes +++", f"Task triggered: {triggered_rule}")
            print("+++ yaes +++", emit_triggered_event(event_data, triggered_rule))
        sleep(0.5)

if __name__ == "__main__":
    start()
