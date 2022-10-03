# Typeform Interview

This repository contains the code for the YAES task set by Typeform.

### Running YAES
In one console, get kafka and zookeeper running:

```
docker-compose up
```

In another console, run `yaes/main.py`:

```
python yaes/main.py
```

For the purpose of this technical test, I have not added YAES to the docker-compose file as it was easier and faster to do it directly via the console. I have left the Dockerfile I was initially going to use however in the repository.

### Trigger Rules
Trigger rules are currently very simple, they consist of a trigger name `trigger_rule` and a task name `task_name`. Any task that is ingested with a task name that refers to a given rule will be sent to the `task.trigger` topic.

Next steps for improving the triggers would be making them more complex and including various options for different types of rules. For example, more complex rules could include an operator (e.g. `=` / `is_in` / `regex_match`) that are processed dynamically for different aspects of the payload (e.g. `payload_key`).

I've left the trigger rules as a JSON file as that can be updated in multiple ways. For example, a UI could be built where the rules can be defined, this has the added benefit of being able to enforce rules that the validation step can test against. Next steps for the creation of these rules is to isolate them from YAES itself, as in its current form it requires updating the git repository. I would put them in some form of S3 bucket which YAES checks against on a scheduled basis i.e. 1 hour.

### Infrastructure
For the purpose of this test, I've left it really simple, but here are some notes on how to make it more "production ready":

- Isolate services in their own environments i.e. have a separate kafka and zookeeper service on AWS, could use AWS hosted version of kafka for this to save setup costs
- Introduce backup options for events i.e. lambda architecture
