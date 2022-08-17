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

class InjectionAddForm(FlaskForm):
    """Form for adding an injection."""

    method = SelectField(
      'Method',
      choices=[('subq', 'Subcutaneous'), ('im','Intramuscular')]
    )
    body_region = SelectField(
      'Body region',
      choices=[('1', 'Abdomen'), ('2','Thigh')]
    )
    position = SelectField(
      'Injection position',
      choices=[('1', 'Left, upper'), ('2','Right, lower')]
    )
    occurred_at = DateTimeField('Date of Injection')
    notes = StringField("Notes?")