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

cwd = os.getcwd()
UPLOAD_FOLDER = cwd + '\\www'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
UPLOAD_FOLDER ='C:/Users/maksa/Documents/projects/DataGurus'

app.layout = html.Div( 
        children=[
            html.Iframe(id='iframe-upload',src=f'/upload'),
            html.Div(id='output')
                ]
)

@app.server.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)

        df = pd.read_csv(request.files['file'].stream._file, encoding='shift-jis')

        print(df)
        #file.save(os.path.join(UPLOAD_FOLDER, filename))

    return '''
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
if __name__ == '__main__':
   app.run_server(debug=True)