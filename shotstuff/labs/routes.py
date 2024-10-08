from flask import Blueprint, flash, render_template, redirect
from flask_login import current_user, login_required

from shotstuff.database import db
from shotstuff.labs.models import Lab
from shotstuff.injections.models import Injection
from shotstuff.labs.forms import LabEditForm, LabAddForm

labs = Blueprint(
    "labs",
    __name__,
    template_folder='templates'
)

#TODO: need to decide what these endpoints should actually look like and
# make sure they're consistent with the other modules (treatments, etc)
@labs.route("/users/<int:user_id>")
@login_required
def list_labs(user_id):
    """
    Render template with all user labs.
    """

    logged_in_user_id = current_user.get_id()

    if not logged_in_user_id != user_id:
        flash("Unauthorized")
        return redirect(f"/users/{logged_in_user_id}")

    # TODO: all of these types routes rely on the data of the logged-in user to
    # populate the templates. If there are ever admin users who can view/edit data
    # of other users, this will need to be updated so that we don't automatically
    # see the information of the person logged in.

    return render_template(
        "/labs/list_labs.html",
        user=current_user,
    )

@labs.route("/users/<int:user_id>/<int:lab_id>", methods=["GET", "POST"])
@login_required
def mark_lab_complete(user_id, lab_id):
    """
    Updates a targeted lab instance's is_upcoming status from True to False.
    Redirects back to that user's lab listing page.
    """

    logged_in_user_id = current_user.get_id()

    if not logged_in_user_id != user_id:
        flash("Unauthorized")
        return redirect(f"/users/{logged_in_user_id}")

    lab = Lab.query.get_or_404(lab_id)
    form = LabEditForm()

    if form.validate_on_submit():
        # update existing lab record with form data
        lab.point_in_cycle_occurred = form.point_in_cycle_occurred.data
        lab.occurred_at = form.occurred_at.data
        lab.completed_on_time = True if (
            lab.occurred_at <= lab.treatment.next_lab_due_date
        ) else False

        # update treatment to store next lab due date and create new upcoming lab
        lab.treatment.update_next_lab_due_date()
        db.session.commit()

        flash("Thanks for your updates! Next routine lab added.")

        return redirect(f"/labs/users/{logged_in_user_id}")

    return render_template(
        "labs/edit_lab_form.html",
        form=form,
        lab=lab
    )

@labs.route("/users/<int:user_id>/new", methods=['GET', 'POST'])
@login_required
def add_lab(user_id):
    """
    If GET, display form to add new lab for logged-in user.

    If POST, adds new lab for the user.
    """

    form = LabAddForm()

    treatment_tuples = [
        (t.id, t.medication_regimen.title) for t in current_user.active_treatments
    ]
    form.treatment_id.choices = treatment_tuples

    if form.validate_on_submit():
        lab = Lab(
            treatment_id = form.treatment_id.data,
            is_routine_lab = form.is_routine_lab.data,
            is_supplemental_lab = form.is_supplemental_lab.data,
            requires_fasting = form.requires_fasting.data,
            occurred_at = form.occurred_at.data or None,
            point_in_cycle_occurred = form.point_in_cycle_occurred.data or None
        )
        db.session.add(lab)
        db.session.commit()

        flash("New lab added!")

        return redirect(f"/labs/users/{current_user.get_id()}")

    return render_template(
        "labs/add_lab_form.html",
        form=form,
    )