import base64
from fileinput import filename
import io
from os.path import join
import uuid
from flask import Flask, flash, request
import pandas as pd
from werkzeug.utils import secure_filename
import dash
from dash import html, Output, Input, State
import os
from io import StringIO
from .dash import Dash
import dash_uploader as du
from pathlib import Path

cwd = os.getcwd()
UPLOAD_FOLDER_ROOT = cwd + '\\www'
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# UPLOAD_FOLDER ='C:/Users/maksa/Documents/projects/DataGurus'


def get_upload_component(id):
    return du.Upload(
        id=id,
        max_file_size=1800,  # 1800 Mb
        filetypes=['csv', 'zip'],
        chunk_size=1800,  # 100 Mb
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


def callback_on_completion(iscompleted, filenames, upload_id):
    if not iscompleted:
        return

    out = []
    if filenames is not None:
        if upload_id:
            root_folder = Path(UPLOAD_FOLDER_ROOT) / upload_id
        else:
            root_folder = Path(UPLOAD_FOLDER_ROOT)

        for filename in filenames:
            file = root_folder / filename
            out.append(file)
        return html.Ul([html.Li(str(x)) for x in out])

    return html.Div("No Files Uploaded Yet!")


def init_callbacks(dash_app):
    dash_app.app.callback(
        Output('callback-output', 'children'),
        [Input('dash-uploader', 'isCompleted')],
        [State('dash-uploader', 'fileNames'),
        State('dash-uploader', 'upload_id')],
    ),
    (callback_on_completion)


def init_dash(flask_server):

    stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    """Create a Plotly Dash dashboard."""
    dash_app = Dash(server=flask_server, routes_pathname_prefix="/fileuploader/", external_stylesheets=stylesheets)

    # 1) configure the upload folder
    du.configure_upload(dash_app, UPLOAD_FOLDER_ROOT)

    # create dash layout
    dash_app.layout = app_layout

    # initialize callbacks
    # init_callbacks(dash_app)

    return dash_app

# if __name__ == '__main__':
#    init_dash(app)
#    app.run_server(debug=True, port=8050)