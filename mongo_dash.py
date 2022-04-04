from fileinput import filename
from typing import Collection
import dash     # need Dash version 1.21.0 or higher
from dash import Input, Output, State, dcc, html, callback, dash_table

import base64
import datetime
import io
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import pymongo
from pymongo import MongoClient
from bson import ObjectId

# Connect to local server
client = MongoClient("mongodb+srv://dash:Dash1234@cluster0.jipdo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

# Create database called animals
mydb = client["Maksad"]
# Create Collection (table) called shelterA
collection = mydb["default"]
upload_filename = ""
docs = {"id":1, "name":"Drew"}
collection.insert_one(docs)

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([
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
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    html.Div([
        dcc.Input(
            id='adding-rows-name',
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

    html.Button("Save to Mongo Database", id="save-it"),

    html.Button('Add Row', id='adding-rows-btn', n_clicks=0),

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


    html.Div(id="show-graphs", children=[]),
    # html.Div(id="placeholder")

])


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    global upload_filename
    #collection = mydb[filename]
    upload_filename = filename
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
        html.H5(filename),
        # dash_table.DataTable(
        #     data=df.to_dict('records'),
        #     columns=[{'name': i, 'id': i} for i in df.columns],
        #     page_size=15
        # ),
         dash_table.DataTable(
            id='my-table',
            columns=[{
                'name': x,
                'id': x,
            } for x in df.columns],
            data=df.to_dict('records'),
            editable=True,
            row_deletable=True,
            filter_action="native",
            filter_options={"case": "sensitive"},
            sort_action="native",  # give user capability to sort columns
            sort_mode="single",  # sort across 'multi' or 'single' columns
            page_current=0,  # page number that user is on
            page_size=15,  # number of rows visible per page
            style_cell={'textAlign': 'left', 'minWidth': '100px',
                        'width': '100px', 'maxWidth': '100px'},
        ),
        dcc.Store(id='stored-data', data=df.to_dict('records')),

    ])

@app.callback(Output('file-datatable', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'))

def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

# def import_content(filepath):
#     mng_client = pymongo.MongoClient('localhost', 27017)
#     mng_db = mng_client['mongodb_name'] // Replace mongo db name
#     collection_name = 'collection_name' // Replace mongo db collection name
#     db_cm = mng_db[collection_name]
#     cdir = os.path.dirname(__file__)
#     file_res = os.path.join(cdir, filepath)

#     data = pd.read_csv(file_res)
#     data_json = json.loads(data.to_json(orient='records'))
#     db_cm.remove()
#     db_cm.insert(data_json)

# Display Datatable with data from Mongo database *************************
@app.callback(Output('mongo-datatable', 'children'),
              [Input('interval_db', 'n_intervals')])
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
                page_size=6,  # number of rows visible per page
                style_table={'height': '300px', 'overflowY': 'auto'},
                style_cell={'textAlign': 'left', 'minWidth': '100px', 'width': '100px', 'maxWidth': '100px'},
                export_format='csv',
                export_headers='display',
                merge_duplicate_headers=True
            )
        ]


# Add new rows to DataTable ***********************************************
@app.callback(
    Output('my-table', 'data'),
    [Input('adding-rows-btn', 'n_clicks')],
    [State('my-table', 'data'),
     State('my-table', 'columns')],
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows

#Add new column
@callback(
    Output('my-table', 'columns'),
    [Input('adding-columns-button', 'n_clicks')],
    [State('adding-rows-name', 'value'),
     State('my-table', 'columns')],
)
def add_columns(n_clicks, value, existing_columns):
    #print(existing_columns)
    if n_clicks > 0:
        existing_columns.append({
            'name': value, 'id': value,
            'renamable': True, 'deletable': True
        })
    #prinlt(existing_columns)
    return existing_columns


# Save new DataTable data to the Mongo database ***************************
@app.callback(
    Output("alert-auto", "is_open"),
    Input("save-it", "n_clicks"),
    State("my-table", "data"),
    State("alert-auto", "is_open"),
    prevent_initial_call=True
)
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


# Create graphs from DataTable data ***************************************
# @app.callback(
#     Output('show-graphs', 'children'),
#     Input('my-table', 'data')
# )
# def add_row(data):
#     df_grpah = pd.DataFrame(data)
#     fig_hist1 = px.histogram(df_grpah, x='age',color="animal")
#     fig_hist2 = px.histogram(df_grpah, x="neutered")
#     return [
#         html.Div(children=[dcc.Graph(figure=fig_hist1)], className="six columns"),
#         html.Div(children=[dcc.Graph(figure=fig_hist2)], className="six columns")
#     ]


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)