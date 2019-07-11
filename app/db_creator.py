from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///ac-control2.db', echo=True)
Base = declarative_base()


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

# create tables
Base.metadata.create_all(engine)