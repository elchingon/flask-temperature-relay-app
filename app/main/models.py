from ..data import CRUDMixin, db

class TemperatureSensor(CRUDMixin, db.Model):
  __tablename__ = "temperature_sensor"

  # Columns
  title = db.Column(db.String(128))
  sensor_id = db.Column(db.String(128))
  min_temp = db.Column(db.Float, default=25.5)
  max_temp = db.Column(db.Float, default=27.5)
  
  def __repr__(self):
    return "<Sensor #{:d}>".format(self.id)