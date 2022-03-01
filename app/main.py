from flask import Blueprint, current_app as app
from flask import render_template
from pygments.formatters.html import HtmlFormatter
from markupsafe import Markup
from flask_login import current_user, login_required, login_user, logout_user


main = Blueprint('main', __name__)


@main.route("/")
def index():
    with open("README.md", "r") as fp:
        formatter = HtmlFormatter(
            style="solarized-dark", full=True, cssclass="codehilite",
        )
        styles = f"<style>{formatter.get_style_defs()}</style>"
       
        return render_template(
            "index.html", styles=Markup(styles),
        )

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)