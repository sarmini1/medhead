from flask import Blueprint, flash, render_template, redirect
from flask_login import current_user, login_required

from shotstuff.users.models import User

users = Blueprint(
    "users",
    __name__,
    template_folder='templates')

# TODO: need to customize unauthorized handler for when login_required fails
@users.route('/dashboard')
@login_required
def dashboard():
    """Show dashboard:

    - anon users: some sort of welcome page w/ buttons to login/signup
    - logged in: that user's treatments

    """
    # breakpoint()
    # if not current_user.is_authenticated:
    #     flash("Unauthorized")
    #     return redirect(f"/users/{current_user.get_id()}")
    return render_template('users/dashboard.html')