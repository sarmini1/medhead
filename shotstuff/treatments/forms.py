from flask_wtf import FlaskForm
from wtforms import (
  IntegerField,
  SelectField,
  DateTimeField,
  PasswordField,
  BooleanField,
  FloatField,
  DateField
)
from wtforms.validators import DataRequired, NumberRange


class TreatmentAddForm(FlaskForm):
    """Form for adding a treatment."""


    medication_regimen_id = SelectField(
      'Medication',
      choices=[('1', 'testosterone cypionate'), ('2','truvada')]
    )
    # TODO: consider removing this field from the form since that should be
    # stored within the med regimen now
    is_for_injectable = BooleanField(
      'Treatment is for an injectable medication',
      validators=[DataRequired()]
    )
    start_date = DateField('Start date')
    frequency = IntegerField(
      'In days, how often will you take this medication?',
      validators=[DataRequired()]
    )
    requires_labs = BooleanField(
      'Treatment requires labs',
      validators=[DataRequired()]
    )
    lab_frequency_in_months = IntegerField(
      '''
      If labs are required, roughly how frequently, in months, are they?
      Ex: Enter 7 if you will take the medication weekly.'''
      ,
      validators=[NumberRange(0, None, "Please provide a valid number.")]
    )
    # lab_point_in_cycle = SelectField(
    #   """
    #   If labs are required, when in your injection cycle should they occur?
    #   If labs are required but the point in the cycle at which they're done
    #   does not matter, please select N/A.
    #   """,
    #   choices=[('1', 'N/A'), ('2', 'Peak'), ('3','Trough'), ('4', 'Middle')]
    # )
    next_lab_due_date = DateField(
      'If labs are required, when are they next due?'
    )


class TreatmentEditForm(FlaskForm):
    """Form for editing a user treatment. """

    frequency = IntegerField('Frequency (days)', validators=[DataRequired()])

