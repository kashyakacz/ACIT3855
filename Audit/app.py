import connexion 
from connexion import NoContent 
import json
from pykafka import KafkaClient
import yaml
import logging
import logging.config
from flask_cors import CORS, cross_origin
from pykafka.exceptions import SocketDisconnectedError
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

def get_daily_steps(index):
    """Get daily steps in history"""
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
    logger.info("Retrieving daily steps reading at index %d" % index)

    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
       
            if msg['type'] == "report_daily_steps":
                payload = msg
                
            elif msg['type'] != "report_calories_burned":
                pass

        return payload, 200
        
    except SocketDisconnectedError as e:
        logger.error(e)
        consumer.stop()
        consumer.start()

    except:
        logger.error("No more messages found")
    logger.error("Could not find daily steps reading at index %d" % index)
    return { "message": "Not Found"}, 404


def get_calories_burned(index):
    """Get calories burned in history"""
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
    logger.info("Retrieving calories burned reading at index %d" % index)

    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
       
            if msg['type'] == "report_calories_burned":
                payload = msg
                
            elif msg['type'] != "report_daily_steps":
                pass

        return payload, 200

    except SocketDisconnectedError as e:
        logger.error(e)
        consumer.stop()
        consumer.start()

    except:
        logger.error("No more messages found")
    logger.error("Could not find calories burned reading at index %d" % index)
    return { "message": "Not Found"}, 404

app = connexion.FlaskApp(__name__, specification_dir='')
if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    CORS(app.app)
    app.app.config['CORS_HEADERS']='Content-Type'
app.add_api("openapi.yaml", base_path="/audit", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
     app.run(port=8110)