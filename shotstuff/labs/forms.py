from flask_wtf import FlaskForm
from wtforms import (
  StringField,
  IntegerField,
  SelectField,
  DateTimeField,
  PasswordField,
  BooleanField,
  FloatField,
  DateField
)
from wtforms.validators import DataRequired, NumberRange


class LabEditForm(FlaskForm):
    """Form for editing a lab. """

    occurred_at = DateTimeField('Date labs completed')
    point_in_cycle_occurred = SelectField(
      'What point did the lab occur in your cycle?',
      choices=[
        ('peak', 'Peak'),
        ('trough','Trough'),
      ]
    )