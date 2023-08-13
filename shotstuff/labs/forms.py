from flask_wtf import FlaskForm
from wtforms import (
  SelectField,
  BooleanField,
  DateField
)
from wtforms.validators import Optional


class LabEditForm(FlaskForm):
    """Form for editing a lab. """

    occurred_at = DateField('Date labs completed')
    point_in_cycle_occurred = SelectField(
      'What point did the lab occur in your cycle?',
      choices=[
        (None, 'N/A'),
        ('peak', 'Peak'),
        ('trough','Trough'),
      ]
    )


class LabAddForm(FlaskForm):
    """Form for adding a lab."""

    treatment_id = SelectField(
      'Which treatment is this for?',
    )

    is_routine_lab = BooleanField(
        "This is a routine lab. "
    )

    is_supplemental_lab = BooleanField(
        "This is a supplmental lab. "
    )

    requires_fasting = BooleanField(
        "Fasting is required. "
    )

    occurred_at = DateField(
      'If already completed, date completed.',
      validators=[Optional()]
    )

    point_in_cycle_occurred = SelectField(
      'What point did the lab occur in your cycle?',
      choices=[
        (None, 'N/A'),
        ('peak', 'Peak'),
        ('trough','Trough'),
      ]
    )