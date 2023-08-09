from flask_wtf import FlaskForm
from wtforms import (
  StringField,
  SelectField,
  DateTimeLocalField,
)
from wtforms.validators import InputRequired


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
      choices=[
        ('1', 'Left, upper'),
        ('2','Right, lower'),
        ('3','Right, upper'),
        ('4','Left, lower'),
      ]
    )
    occurred_at = DateTimeLocalField(
      'Date and time injection occurred',
      format='%Y-%m-%dT%H:%M',
      validators=[InputRequired()]
    )
    notes = StringField("Notes?")