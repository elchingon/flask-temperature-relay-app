from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String,Float
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
 
engine = create_engine('sqlite:///ac-control2.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
 
class TemperatureSensor(Base):
  __tablename__ = "temperature_sensor"

  # Columns
  id = Column(Integer, primary_key=True)
  title = Column(String(128))
  sensor_id = Column(String(128))
  min_temp = Column(Float, default=25.5)
  max_temp = Column(Float, default=27.5)
  
  def __repr__(self):
    return "<Sensor #{:d}>".format(self.id)


def init_db():
  from .main import models
  from .main.models import TemperatureSensor
  Base.metadata.create_all(bind=engine)