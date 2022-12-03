import connexion
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from base import Base
import requests
from stats import Stats
import yaml
import json
import logging
import logging.config
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS, cross_origin
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

DB_ENGINE = create_engine("sqlite:///stats.sqlite")

Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def get_stats():
    logger.info('Request has been started')
    session = DB_SESSION()
    results = session.query(Stats).order_by(Stats.last_updated.desc())
    if not results:
        logger.error("Statistics does not exist")
        return 404

    logger.info("The request has been completed")
    session.close()
    return results[0].to_dict(), 200

def populate_stats():
    """ Periodically update stats """
    logger.info('processing has been started')
    session = DB_SESSION()
    results = session.query(Stats).order_by(Stats.last_updated.desc())
    try:
        last_updated = str(results[0].last_updated)
        a,b = last_updated.split(" ")
        url1 = app_config["dailySteps"]["url"]+a+'T'+b
        url2 = app_config["caloriesBurned"]["url"]+a+'T'+b
    
    except IndexError:
        last_updated = '2016-08-29T09:12:33.001000'
        url1 = app_config["dailySteps"]["url"]+last_updated
        url2 = app_config["caloriesBurned"]["url"]+last_updated


    headers = {"content-type": "application/json"}

    response_daily_steps = requests.get(url1, headers=headers)
    response_calories_burned = requests.get(url2, headers=headers)

    list_daily_steps = response_daily_steps.json()
    print("list of steps", list_daily_steps)
    list_calories_burned = response_calories_burned.json()

    if response_daily_steps.status_code != 200: 
        logger.error(f"Status code received {response_daily_steps.status_code}")
    
    try:
        min_daily_steps = results[0].min_daily_steps 
        min_calories_burned = results[0].min_calories_burned
        max_daily_steps = results[0].max_daily_steps
        max_calories_burned = results[0].max_calories_burned

    except IndexError:
        min_daily_steps = 0
        min_calories_burned = 0
        max_daily_steps = 0
        max_calories_burned = 0

    last_updated = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    session = DB_SESSION()

   
    for i in list_daily_steps:
        if i["daily_steps"] < min_daily_steps:
            min_daily_steps = i["daily_steps"]
    
    for i in list_calories_burned:
        if i["calories_burned"] < min_calories_burned:
            min_calories_burned = i["calories_burned"]
        #min_calories_burned = min(min_calories_burned, i["calories_burned"])
  
    for i in list_daily_steps:
        if i["daily_steps"] > max_daily_steps:
            max_daily_steps = i["daily_steps"]

    for i in list_calories_burned:
        if i["calories_burned"] > max_calories_burned:
            max_calories_burned = i["calories_burned"]

 
    session = DB_SESSION()
    stats = Stats(
        min_daily_steps,
        min_calories_burned,
        max_daily_steps,
        max_calories_burned,
        datetime.datetime.strptime(last_updated, "%Y-%m-%dT%H:%M:%S.%f"))

    session.add(stats)

    session.commit()
    session.close()

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats, 'interval', seconds=app_config['scheduler']['period_sec'])
    sched.start()

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS']='Content-Type'
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100, use_reloader=False)


