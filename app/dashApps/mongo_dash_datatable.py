from flask import redirect
from .dash import Dash    # need Dash version 1.21.0 or higher
from dash import Input, Output, State, dcc, html, callback, dash_table

import base64
import datetime
import io
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from pymongo import MongoClient
from flask_login import current_user

import sweetviz as sv
from pandas_profiling import ProfileReport

# Connect to local server
client = MongoClient("mongodb+srv://dash:Dash1234@cluster0.jipdo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

# Create database called animals
mydb = client["Maksad"]
# Create Collection (table) called shelterA
collection = mydb["default"]

upload_filename = ""
docs = {"id":1, "name":"Drew"}
collection.insert_one(docs)


n_clicks=0

app_layout = html.Div([



    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
        },
        # Allow multiple files to be uploaded
        multiple=True,

    ),

    html.Div([
        dcc.Input(
            id='adding-columns',
            placeholder='Enter a column name...',
            value='',
            style={'padding': 10}
        ),
        html.Button('Add Column', id='adding-columns-button', n_clicks=0)
    ], style={'height': 50}),


    html.Div(id='file-datatable', children=[]),

    html.Div(id='mongo-datatable', children=[]),

    # activated once/week or when page refreshed
    dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),

     dbc.Button(
            "Save to Mongo",
            id="save-it",
            className="me-1",
            color="primary",
            n_clicks=0,
            style={"margin-left": '20px', 'margin-bottom': '20px'}
        ),
     dbc.Button(
            "Add Row",
            id='adding-rows-btn',
            className="me-1",
            color="primary",
            n_clicks=0,
            style={"margin-left": '20px', 'margin-bottom': '20px'}
        ),

     dbc.Button(
            "Pandas Profiling Report",
            id='adding-graph-btn',
            className="me-1",
            color="primary",
            n_clicks=0,
            style={"margin-left": '20px', 'margin-bottom': '20px'}
        ),

    dbc.Button(
            "Sweet Viz Report",
            id='adding-graph-btn-1',
            className="me-1",
            color="primary",
            n_clicks=0,
            style={"margin-left": '20px', 'margin-bottom': '20px'}
        ),

    html.A("Click here to access Pandas Profiling Report", href='', target="_blank", id='hidden-button', style = dict(display='none')),
    html.A("Click here to access Sweet Viz Report", href='', target="_blank", id='hidden-button-1', style = dict(display='none')),

    # Create notification when saving to db
    dbc.Alert(
            "Successfully saved to database",
            id="alert-auto",
            is_open=False,
            duration=4000,
            style={
            'color': 'primary'
            },
        ),
    
    # html.Div(id="placeholder")

   
])


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    global upload_filename
    global n_clicks

    n_clicks += 1
    #collection = mydb[filename]

    upload_filename = filename

    if n_clicks == 1:
        print("Uploading file: ", filename)
        collection.delete_many({})
        #mydb.drop_collection("default")
        mydb['default'].rename(filename)

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
         dash_table.DataTable(
            id='my-table',
            columns=[{
                'name': x,
                'id': x,
                'renamable': True,
                'deletable': True,
                'editable': True
            } for x in df.columns],
            data=df.to_dict('records'),
            editable=True,
            row_deletable=True,
            filter_action="native",
            filter_options={"case": "sensitive"},
            sort_action="native",  # give user capability to sort columns
            sort_mode="single",  # sort across 'multi' or 'single' columns
            page_current=0,  # page number that user is on
            page_size=12,  # number of rows visible per page
            export_format='csv',
            export_headers='display',
            style_cell={'textAlign': 'left', 'minWidth': '100px',
                        'width': '100px', 'maxWidth': '100px'},
        ),
        dcc.Store(id='stored-data', data=df.to_dict('records')),

    ])

def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        return children

# Display Datatable with data from Mongo database *************************

def populate_datatable(n_intervals):
    print(n_intervals)
    print(collection.name)
    print(mydb.list_collection_names())
    # Convert the Collection (table) date to a pandas DataFrame

    df = pd.DataFrame()

    for collect in mydb.list_collection_names():
        if collect != 'default':
            df = pd.DataFrame(list(mydb[collect].find({})))
            #Drop the _id column generated automatically by Mongo
            df = df.iloc[:, 1:]
            (df.head(20))

    if df.empty:
        return html.Div([
            html.H5("No data found in database")
        ])
    else:
        return [
            dash_table.DataTable(
                id='my-table',
                columns=[{
                    'name': x,
                    'id': x,
                    'deletable': True,
                    'renamable': True,
                } for x in df.columns],


                data=df.to_dict('records'),
                editable=True,
                row_deletable=True,
                filter_action="native",
                filter_options={"case": "sensitive"},
                sort_action="native",  # give user capability to sort columns
                sort_mode="single",  # sort across 'multi' or 'single' columns
                page_current=0,  # page number that user is on
                page_size=12,  # number of rows visible per page
                style_table={'height': '300px', 'overflowY': 'auto'},
                style_cell={'textAlign': 'left', 'minWidth': '100px', 'width': '100px', 'maxWidth': '100px'},
                export_format='csv',
                export_headers='display',
                merge_duplicate_headers=True
            )
        ]


# Add new rows to DataTable ***********************************************
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows

#Add new column
def add_columns(n_clicks, value, existing_columns):
    #print(existing_columns)
    if n_clicks > 0:
        existing_columns.append({
            'name': value, 'id': value,
            'renamable': True, 'deletable': True
        })
    #prinlt(existing_columns)
    return existing_columns, ""


# Save new DataTable data to the Mongo database ***************************
def save_data(n_clicks, data, is_open):
    if n_clicks > 0:
        dff = pd.DataFrame(data)
        print(mydb.list_collection_names())
        
        mydb[upload_filename].delete_many({})
        mydb[upload_filename].insert_many(dff.to_dict('records'))
        print("Data saved to database", mydb[upload_filename].name)
        if n_clicks > 0:
            return not is_open
    return is_open


def make_vizualization_ppr(n_clicks, data):
    if n_clicks > 0:
        dff = pd.DataFrame(data)
        print("making viz")

        try:
            design_report = ProfileReport(dff, title="Pandas Profiling Report")
            design_report.to_file(output_file=f'app/static/{upload_filename}.html')
            return dict(), f'http://127.0.0.1:5000/static/{upload_filename}.html'
        except:
            print("No data found")

def make_vizualization_sweet_viz(n_clicks, data):
    if n_clicks > 0:
        dff = pd.DataFrame(data)
        print("making viz")

        try:
            sweet_report = sv.analyze(dff)
            sweet_report.show_html(f'app/static/{upload_filename}.html')

            return dict(), f'http://127.0.0.1:5000/static/{upload_filename}.html'
        except:
            print("No data found")


def init_callbacks(dash_app):
    dash_app.callback(
        Output('file-datatable', 'children'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
    )(update_output)
    dash_app.callback(
        Output('mongo-datatable', 'children'),
        Input('interval_db', 'n_intervals'))
    (populate_datatable)
    dash_app.callback(
        Output('my-table', 'data'),
        Input('adding-rows-btn', 'n_clicks'),
        State('my-table', 'data'),
        State('my-table', 'columns'),
    )(add_row)
    dash_app.callback(
        Output('my-table', 'columns'),
        Output('adding-columns', 'value'),
        Input('adding-columns-button', 'n_clicks'),
        State('adding-columns', 'value'),
        State('my-table', 'columns'),
    )(add_columns)
    dash_app.callback(
        Output("hidden-button", "style"),
        Output("hidden-button", "href"),
        Input("adding-graph-btn", "n_clicks"),
        State('my-table', 'data'),
    )(make_vizualization_ppr)
    dash_app.callback(
        Output("hidden-button-1", "style"),
        Output("hidden-button-1", "href"),
        Input("adding-graph-btn-1", "n_clicks"),
        State('my-table', 'data'),
    )(make_vizualization_sweet_viz)
    dash_app.callback(
        Output("alert-auto", "is_open"),
        Input("save-it", "n_clicks"),
        State("my-table", "data"),
        State("alert-auto", "is_open"),
        prevent_initial_call=True
    )(save_data)
   

    return dash_app

def init_dash(flask_server, current_user):
    """Create a Plotly Dash dashboard."""
    dash_app = Dash(server=flask_server, routes_pathname_prefix="/mongo_dash/", external_stylesheets=['assets/bWLwgP.css'])

    # create dash layout
    dash_app.layout = app_layout

    # initialize callbacks
    init_callbacks(dash_app)

    print("This is current session user:", current_user)

    return dash_app

# if __name__ == '__main__':
#     app.run_server(debug=True, port=8080)
