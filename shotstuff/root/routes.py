from flask import (
    Blueprint,
    render_template,
    redirect,
    flash,
    request,
    url_for,
    abort,
)
from flask_login import login_user, current_user, login_required, logout_user
from is_safe_url import is_safe_url

from shotstuff.database import db
from shotstuff.users.models import User
from shotstuff.root.forms import LoginForm, RegisterForm
from shotstuff.generic_forms import CSRFProtection

root = Blueprint(
    "root",
    __name__,
    template_folder='templates'
)

@root.get('/')
def homepage():
    """Show homepage:

    - anon users: some sort of welcome page w/ buttons to login/signup
    - logged in: that user's dashboard
    """
    # Note to self: we get this current_user object from flask-login, which seems
    # to be accessible in every template and in every subsequent request??

    if current_user.is_authenticated:
        #returning a redirect for now but ideally should consolidate the
        # treatment listing page to this?
        return redirect(f"/users/dashboard")

    else:
        return render_template('home-anon.html')

@root.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login.

    If GET, renders form to login.

    If POST, validates form and redirects to next location, if safe.
    """

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            form.username.data,
            form.password.data
        )
        if user:
            login_user(user)
            flash(f"Hello, {user.username}!", "success")

            next = request.args.get('next')

            if not is_safe_url(next, {"localhost:5000"}):
                # breakpoint()
                return abort(400)

            return redirect(next or url_for('/users/dashboard'))

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)

@root.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user registration.

    If GET, renders form to register.

    If POST, validates form and redirects to next location, if safe.
    """

    form = RegisterForm()

    if form.validate_on_submit():
        user = User.signup(
            form.username.data,
            form.password.data,
            form.first_name.data
        )
        if user:
            db.session.commit()
            login_user(user)
            flash(f"Hello, {user.username}!", "success")

            next = request.args.get('next')

            if not is_safe_url(next, {"localhost:5000"}):
                # breakpoint()
                return abort(400)

            return redirect(next or url_for('/users/dashboard'))

        flash("Invalid credentials.", 'danger')

    return render_template('users/signup.html', form=form)

@root.route("/logout", methods=["POST"])
@login_required
def logout():

    form = CSRFProtection()

    if form.validate_on_submit():
        logout_user()
        flash("Successfully logged out!")
        return redirect('/login')

    else:
        flash("Access unauthorized.", "danger")
        return redirect("/")
