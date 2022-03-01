from flask import current_app as app
from flask import render_template
from pygments.formatters.html import HtmlFormatter
from markupsafe import Markup


@app.route("/")
def index():
    with open("README.md", "r") as fp:
        formatter = HtmlFormatter(
            style="solarized-dark", full=True, cssclass="codehilite",
        )
        styles = f"<style>{formatter.get_style_defs()}</style>"
       
        return render_template(
            "index.html", styles=Markup(styles),
        )
