from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime
import uuid


class DailySteps(Base):
    """ Daily Steps """

    __tablename__ = "daily_steps"

    
    id = Column(Integer, primary_key=True)
    client_name = Column(String(250), nullable=False)
    age = Column(Integer, nullable=False)
    daily_steps = Column(Integer, nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    trace_id = Column(String(100), nullable=False)

    def __init__(self, client_name, age, daily_steps, timestamp):
        """ Initializes a daily steps reading """
        self.client_name = client_name
        self.age = age
        self.daily_steps = daily_steps
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()
        self.trace_id = uuid.uuid4()

    def to_dict(self):
        """ Dictionary Representation of daily steps for the day """
        dict = {}
        dict['id'] = self.id
        dict['client_name'] = self.client_name
        dict['age'] = self.age
        dict['daily_steps'] = self.daily_steps
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created
        dict['trace_id'] = self.trace_id

        return dict
