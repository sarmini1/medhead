from flask import Blueprint, flash, render_template, redirect
from flask_login import current_user, login_required

from shotstuff.database import db
from shotstuff.treatments.models import Treatment
from shotstuff.injections.models import Injection
from shotstuff.treatments.forms import TreatmentAddForm, TreatmentEditForm
from shotstuff.injections.forms import InjectionAddForm

treatments = Blueprint(
    "treatments",
    __name__,
    template_folder='templates')


@treatments.route("/", methods=['GET', 'POST'])
@login_required
def add_treatment():
    """
    If GET, display form to add new treatment for logged-in user.

    If POST, adds new treatment for the user.
    """

    form = TreatmentAddForm()

    if form.validate_on_submit():
        treatment = Treatment(
            user_id = g.user.id,
            is_for_injectable = form.is_for_injectable.data,
            injection_regimen_id = form.injection_regimen_id.data,
            currently_active = form.currently_active.data,
            start_date = form.start_date.data,
            frequency_in_seconds = int(form.frequency.data) * 86400,
            requires_labs = form.requires_labs.data,
            lab_frequency_in_months = form.lab_frequency_in_months.data,
            # lab_point_in_cycle = form.lab_point_in_cycle.data,
            next_lab_due_date = form.next_lab_due_date.data,
        )
        db.session.add(treatment)
        db.session.commit()

        flash("New treatment added!")

        return redirect(f"/users/treatments/{current_user.get_id()}")

    return render_template(
        "treatments/add_treatment_form.html",
        form=form,
    )


@treatments.route("/users/<int:user_id>")
@login_required
def list_user_treatments(user_id):
    """
    Render template with all user treatments.
    """

    logged_in_user_id = current_user.get_id()

    if not logged_in_user_id != user_id:
        flash("Unauthorized")
        return redirect(f"/users/{logged_in_user_id}")

    return render_template(
        "/treatments/user_treatments.html",
        user=current_user
    )


@treatments.route("/<int:treatment_id>")
@login_required
def display_treatment_detail(treatment_id):
    """TBD"""

    treatment = Treatment.query.get_or_404(treatment_id)
    next_injection_date = treatment.next_injection_time
    next_injection_dow = next_injection_date["weekday"]
    # total_injections = len(treatment.injections)

    return render_template(
        "treatments/treatment_detail.html",
        treatment=treatment,
        next_injection_date=next_injection_date,
        next_injection_dow=next_injection_dow
        )


@treatments.route("/<int:treatment_id>/update", methods=['GET', 'POST'])
@login_required
def edit_treatment(treatment_id):
    """
    Edit a treatment. Display form if GET, otherwise validate and commit changes.
    """

    treatment = Treatment.query.get_or_404(treatment_id)

    logged_in_user_id = current_user.get_id()

    if not logged_in_user_id != treatment.user.id:
        flash("Unauthorized")
        return redirect(f"/users/{logged_in_user_id}")

    form = TreatmentEditForm()

    if form.validate_on_submit():
        treatment.frequency_in_seconds = form.frequency.data*86400
        db.session.commit()

        flash("Thanks for your updates!")

        return redirect(f"/treatments/{treatment_id}")

    return render_template(
        "treatments/edit_treatment_form.html",
        form=form,
        treatment=treatment)


@treatments.route("/<int:treatment_id>/injections", methods=['GET', 'POST'])
def add_injection(treatment_id):
    """Add an injection. Display form if GET, otherwise validate and add message."""

    form = InjectionAddForm()
    treatment = Treatment.query.get_or_404(treatment_id)

    if form.validate_on_submit():
        injection = Injection(
            treatment_id = treatment_id,
            medication_id = treatment.injection_regimen.medication_id,
            method = form.method.data,
            body_region_id = form.body_region.data,
            position_id = form.position.data,
            occurred_at = form.occurred_at.data,
            notes = form.notes.data
        )
        db.session.add(injection)
        db.session.commit()

        flash("Nice job taking care of yourself!")

        return redirect(f"/treatments/{treatment_id}")

    return render_template(
        "injections/add_injection_form.html",
        form=form,
        treatment=treatment
        )