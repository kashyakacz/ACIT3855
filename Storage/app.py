import connexion
import datetime
import uuid
import yaml
import json
import logging
import logging.config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from connexion import NoContent
from daily_steps import DailySteps
from calories_burned import CaloriesBurned
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread 


with open('app_conf.yml', 'r') as f:
  app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
  log_config = yaml.safe_load(f.read())
  logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

DB_ENGINE = create_engine('mysql+pymysql://root:password@acit3855-lab6.westus3.cloudapp.azure.com:3306/events')
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)
logger.info("Connecting to DB. Hostname:%s, Port:%d" %(app_config['events']['hostname'], app_config['events']['port'])) 

trace_id  = uuid.uuid4

# def report_daily_steps(body):
#     """"Recieves a daily steps number event """

  
#     session = DB_SESSION()
#     print(body)
#     ds = DailySteps(body['client_name'],
#                        body['age'],
#                        body['daily_steps'],
#                        body['timestamp'])
#     session.add(ds) 

#     session.commit()
#     session.close()

    
#     logger.info(f'Returned event daily steps response with a trace id of {str(trace_id)}')

#     session.close()

#     return NoContent, 201


# def report_calories_burned(body):
#     """Recieves a daily calories burned number event"""
#     print(body)
    
#     session = DB_SESSION()
#     print(body)
#     cb = CaloriesBurned(body['client_name'],
#                    body['age'],
#                    body['calories_burned'],
#                    body['timestamp'])


#     session.add(cb)

#     session.commit()
#     session.close()

#     logger.info(f'Returned event daily steps response with a trace id of {str(trace_id)}')

#     return NoContent, 201

def get_daily_steps_readings(timestamp):
  """Gets daily steps readings with timestamp"""
  
  session =  DB_SESSION()

  timestamp_date = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")
  dailyS_readings = session.query(DailySteps).filter(DailySteps.date_created >=  timestamp_date)
  dailyS = []
  
  for reading in dailyS_readings:
    dailyS.append(reading.to_dict())
  
  session.close()

  logger.info("Query for daily steps readings after %s returns %d results" %(timestamp, len(dailyS)))
  print(dailyS)
  
  return dailyS, 200


def get_calories_burned_readings(timestamp):
  """Gets calories burned readings with timestamp"""
  
  session =  DB_SESSION()

  timestamp_date = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")
  caloriesB_readings = session.query(CaloriesBurned).filter(CaloriesBurned.date_created >=  timestamp_date)
  caloriesB = []

  for reading in caloriesB_readings:
    caloriesB.append(reading.to_dict())
  
  session.close()

  logger.info("Query for calories burned readings after %s returns %d results" %(timestamp, len(caloriesB)))
  
  return caloriesB, 200

def process_messages():
  """Process event messages"""

  hostname = "%s:%d" % (app_config["events"]["hostname"],
                        app_config["events"]["port"])
  client = KafkaClient(hosts=hostname)
  topic = client.topics[str.encode(app_config["events"]["topic"])]

  consumer = topic.get_simple_consumer(consumer_group=b'event_group', reset_offset_on_start=False, auto_offset_reset=OffsetType.LATEST)

  for msg in consumer: 
    msg_str = msg.value.decode('utf-8')
    msg = json.loads(msg_str)
    logger.info("Message: %s" % msg)
    
    payload = msg["payload"]
    
    if msg["type"] == "report_daily_steps":
      session = DB_SESSION()

      ds = DailySteps(msg['payload']['client_name'],
                        msg['payload']['age'],
                        msg['payload']['daily_steps'],
                        msg['payload']['timestamp'],
                        msg['payload']['trace_id'])

      session.add(ds)
      session.commit()
      session.close()

      trace_id = msg['payload']['trace_id']
      logger.info(f'Stored event daily steps event request with a trace id of {str(trace_id)}')

    elif msg["type"] == "report_calories_burned":
      session = DB_SESSION()

      cb = CaloriesBurned(msg['payload']['client_name'],
                        msg['payload']['age'],
                        msg['payload']['calories_burned'],
                        msg['payload']['timestamp'],                   
                        msg['payload']['trace_id'])

      session.add(cb)

      session.commit()
      session.close()
      trace_id = msg['payload']['trace_id']
      logger.info(f'Stored event calories burned event request with a trace id of {str(trace_id)}')

    consumer.commit_offsets()

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)