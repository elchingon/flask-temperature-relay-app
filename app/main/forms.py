from flask_wtf import FlaskForm
from wtforms import fields, validators
from wtforms.validators import DataRequired

class TemperatureSensorForm(FlaskForm):
  temp1_sensor_id = fields.StringField()
  temp1_min_temp = fields.DecimalField(validators=[DataRequired()])
  temp1_max_temp = fields.DecimalField(validators=[DataRequired()])
  
  temp2_sensor_id = fields.StringField()
  temp2_min_temp = fields.DecimalField(validators=[DataRequired()])
  temp2_max_temp = fields.DecimalField(validators=[DataRequired()])
  
  temp3_sensor_id = fields.StringField()
  temp3_min_temp = fields.DecimalField(validators=[DataRequired()])
  temp3_max_temp = fields.DecimalField(validators=[DataRequired()])