import os
import uuid
from flask import Blueprint, current_app as app
from flask import render_template, request
import pandas as pd
from pygments.formatters.html import HtmlFormatter
from markupsafe import Markup
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from dash import html
import dash_uploader as du

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



def get_upload_component(id):
    return du.Upload(
        id=id,
        max_file_size=1800,  # 1800 Mb
        filetypes=['csv', 'zip'],
        upload_id=uuid.uuid1(),  # Unique session id
    )


app_layout = html.Div(
        [
            html.H1('Demo'),
            html.Div(
                [
                    get_upload_component(id='dash-uploader'),
                    html.Div(id='callback-output'),
                ],
                style={  # wrapper div style
                    'textAlign': 'center',
                    'width': '600px',
                    'padding': '10px',
                    'display': 'inline-block'
                }),
        ],
        style={
            'textAlign': 'center',
        },
    )


@main.route('/API/resumable', methods=['GET', 'POST'])
def upload_file():
    cwd = os.getcwd()
    UPLOAD_FOLDER = cwd + '\\www'
  
    # UPLOAD_FOLDER ='C:/Users/maksa/Documents/projects/DataGurus'
    if request.method == 'POST':
        # file = request.files['file']
        # filename = secure_filename(file.filename)
        print(request.files['file'].stream._file)
        df = pd.read_csv(request.files['file'].stream._file, encoding='shift-jis')

        print(df)
        # file.save(os.path.join(UPLOAD_FOLDER, filename))
    return '''
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''