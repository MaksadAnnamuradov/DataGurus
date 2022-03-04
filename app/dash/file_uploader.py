import base64
import io
from os.path import join
from flask import Flask, flash, request
import pandas as pd
from werkzeug.utils import secure_filename
import dash
from dash import html
import os
from io import StringIO
from .dash import Dash


app_layout = html.Div( 
        children=[
            html.H1("Upload File"),
            html.Iframe(id='iframe-upload',src=f'/upload', height='300', width='300'),
            html.Div(id='output')
                ]
)


def init_dash(flask_server):
    """Create a Plotly Dash dashboard."""
    dash_app = Dash(server=flask_server, routes_pathname_prefix="/file/")

    # create dash layout
    dash_app.layout = app_layout

    # initialize callbacks
    # init_callbacks(dash_app)

    return dash_app


# if __name__ == '__main__':
#    app.run_server(debug=True)