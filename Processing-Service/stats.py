from sqlalchemy import Column, Integer, String, DateTime
from base import Base

class Stats(Base):
    """Statistics """

    __tablename__ = "stats"

    id = Column(Integer, primary_key=True)
    min_daily_steps = Column(Integer, nullable=False)
    min_calories_burned = Column(Integer, nullable=True)
    max_daily_steps = Column(Integer, nullable=True)
    max_calories_burned = Column(Integer, nullable=True)
    last_updated = Column(DateTime, nullable=False)

    def __init__(self, min_daily_steps, min_calories_burned, max_daily_steps, max_calories_burned,last_updated):
        """ Initializes a processing statistics objet """
        self.min_daily_steps = min_daily_steps
        self.min_calories_burned = min_calories_burned
        self.max_daily_steps = max_daily_steps
        self.max_calories_burned = max_calories_burned
        self.last_updated = last_updated
        

    def to_dict(self):
        """ Dictionary Representation of a statistics """
        dict = {}
        dict['min_daily_steps'] = self.min_daily_steps
        dict['min_calories_burned'] = self.min_calories_burned
        dict['max_daily_steps'] = self.max_daily_steps
        dict['max_calories_burned'] = self.max_calories_burned
        dict['last_updated'] = self.last_updated.strftime("%Y-%m-%dT%H:%M:%S.%f") #07/28/2014 18:54:55.099
        
        return dict