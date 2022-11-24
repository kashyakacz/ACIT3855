from http import client
from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime
import uuid


class CaloriesBurned(Base):
    """ Calories Burned """

    __tablename__ = "calories_burned"


    id = Column(Integer, primary_key=True)
    client_name = Column(String(250), nullable=False)
    age = Column(Integer, nullable=False)
    calories_burned = Column(Integer, nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    trace_id = Column(String(100), nullable=False)

    def __init__(self, client_name, age, calories_burned, timestamp):
        """ Initializes a calories burned reading """
        self.client_name = client_name
        self.age = age
        self.calories_burned = calories_burned
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()
        self.trace_id = uuid.uuid4()

    def to_dict(self):
        """ Dictionary Representation of calories burned reading """
        dict = {}
        dict['id'] = self.id
        dict['client_name'] = self.client_name
        dict['age'] = self.age
        dict['calories_burned'] = self.calories_burned
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created
        dict['trace_id'] = self.trace_id

        return dict