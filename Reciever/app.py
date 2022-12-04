import connexion
import requests
from connexion import NoContent 
import json
import datetime
import os
import yaml
import logging
import logging.config
import uuid
from pykafka import KafkaClient
from pykafka.exceptions import SocketDisconnectedError, LeaderNotFoundError
import os

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"

with open(app_conf_file, 'r') as f:
  app_config = yaml.safe_load(f.read())

# External Logging Configuration
with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)

def report_daily_steps(body):
    """Recieves a daily steps request"""
    trace_id = uuid.uuid4()

    logging.info (f'Recieved daily steps event request with a trace id of {str(trace_id)}')

    daily_steps_data = {
        "client_name": body['client_name'],
        "age": body["age"],
        "daily_steps": body["daily_steps"],
        "timestamp":body["timestamp"],
        "trace_id": str(trace_id)
    }

    client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()

    msg = {"type": "report_daily_steps",
    "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    "payload": body }
    msg_str = json.dumps(msg)

    try:
        producer.produce(msg_str.encode('utf-8'))

    except (SocketDisconnectedError, LeaderNotFoundError) as e:
        producer = topic.get_sync_producer()
        producer.stop()
        producer.start()
        producer.produce(msg_str.encode('utf-8'))

    response = 201 

    if response == 201:
        logger.info(f'Returned event daily steps response{str(trace_id)} with status {201}')
    
    return NoContent,  201


def report_calories_burned(body):
    """Recieves a calories burned request"""
    trace_id = uuid.uuid4()

    logging.info (f'Recieved calores burned event request with a trace id of {str(trace_id)}')
    # daily_calories_burned = {
    #     "client_name": body['client_name'],
    #     "age": body["age"],
    #     "calories_burned": body["calories_burned"],
    #     "timestamp":body["timestamp"],
    #     "trace_id": str(trace_id)
    # }

    client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()

    msg = {"type": "report_calories_burned",
    "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    "payload": body}
    msg_str = json.dumps(msg)

    try:
        producer.produce(msg_str.encode('utf-8'))

    except (SocketDisconnectedError, LeaderNotFoundError) as e:
        producer = topic.get_sync_producer()
        producer.stop()
        producer.start()
        producer.produce(msg_str.encode('utf-8'))


    response = 201 
 
    if response == 201:
        logger.info(f'Returned event daily steps response{str(trace_id)} with status {201}')
    
    return NoContent,  201

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", base_path="/receiver",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)