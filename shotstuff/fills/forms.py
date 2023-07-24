from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField


class FillAddForm(FlaskForm):
    """Form for adding an medication fill."""

    occurred_at = DateField('Date fill occurred')
    filled_by = StringField('Pharmacy who filled')
    days_supply = IntegerField('Days supply')
    notes = StringField("Notes?")