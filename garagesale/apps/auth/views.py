from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_babel import gettext as _
from flask_login import login_user, logout_user, login_required

from garagesale.extensions import login_manager

from .forms import LoginForm
from .models import User

blueprint = Blueprint(
    "auth",
    __name__,
    static_folder="../static",
    template_folder="templates"
)


@login_manager.user_loader
def load_user(user_id):
    """ Define the user loader (required by flask-login) """

    return User.get_by_id(int(user_id))


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    """ Login view """

    form = LoginForm(request.form)

    if request.method == "POST":
        if form.validate_on_submit():
            login_user(form.user)
            flash(_("You are logged in."), "success")
            redirect_url = request.args.get("next") or url_for("public.index")
            return redirect(redirect_url)
        else:
            flash(form)

    return render_template("login.jinja", form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    """ Logout view """

    logout_user()
    flash(_("You are logged out."), "info")
    return redirect(url_for('public.index'))
