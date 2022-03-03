import os
from flask import Blueprint, current_app as app
from flask import render_template, request
import pandas as pd
from pygments.formatters.html import HtmlFormatter
from markupsafe import Markup
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

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

@main.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    cwd = os.getcwd()
    UPLOAD_FOLDER = cwd + '\\www'
  
    UPLOAD_FOLDER ='C:/Users/maksa/Documents/projects/DataGurus'
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)

        df = pd.read_csv(request.files['file'].stream._file, encoding='shift-jis')

        print(df)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

    return '''
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''