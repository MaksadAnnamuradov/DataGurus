import base64
from fileinput import filename
import io
from os.path import join
import uuid
from flask import Flask, flash, request
import pandas as pd
from werkzeug.utils import secure_filename
import dash
from dash import html, Output
import os
from io import StringIO
from .dash import Dash
import dash_uploader as du

# cwd = os.getcwd()
# UPLOAD_FOLDER = cwd + '\\www'
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# # app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# UPLOAD_FOLDER ='C:/Users/maksa/Documents/projects/DataGurus'





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



# @app.server.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         file = request.files['file']
#         filename = secure_filename(file.filename)

#         df = pd.read_csv(request.files['file'].stream._file, encoding='shift-jis')

#         print(df)
#         #file.save(os.path.join(UPLOAD_FOLDER, filename))

#     return '''
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''

# @du.callback(
#     output=Output('callback-output', 'children'),
#     id='dash-uploader',
# )

def get_a_list(filenames):
    return html.Ul([html.Li(filenames)])



def init_callbacks(dash_app):
    dash_app.callback(
       Output('callback-output', 'children'),
            id='dash-uploader',
        ),
    (get_a_list)


def init_dash(flask_server):

    stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    """Create a Plotly Dash dashboard."""
    dash_app = Dash(server=flask_server, routes_pathname_prefix="/file/", external_stylesheets=stylesheets)

        # 1) configure the upload folder
    du.configure_upload(dash_app, r"C:/Users/maksa/Documents/projects/DataGurus", upload_api='/upload')

    # create dash layout
    dash_app.layout = app_layout

    # initialize callbacks
    init_callbacks(dash_app)

    return dash_app

# if __name__ == '__main__':
#    app.run_server(debug=True)