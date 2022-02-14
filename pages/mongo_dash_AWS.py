# Set up guide: https://docs.google.com/document/d/1EdvOK5_1D4ya94-N0RU5t9Rm_e2YurhU/edit?usp=sharing&ouid=118003078876393636228&rtpof=true&sd=true
import dash
from dash import Input, Output, State, dcc, html, callback
from dash import dash_table


import pandas as pd
import plotly.express as px
import pymongo

#from app import app

dash.register_page(__name__)

# from pymongo import MongoClient
# might need to run: pip install "pymongo[srv]"

# Connect to server on the cloud

client = pymongo.MongoClient("mongodb+srv://dash:Dash1234@cluster0.jipdo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

# test connection
db = client.test
print(db)
# exit()


# # test by goining into sample database
# db = client.sample_weatherdata
# # go into its collection (table)
# weather_data = db["data"]
# weather = weather_data.find()
# for x in weather:
#     print(x)
#     break
# exit()


# Go into the database I created
db = client["catlovers"]
# Go into one of my database's collection (table)
collection_shelter = db["shelterNYC"]
# Create the first document (row) in my collection
# record = {
#     "owner": "Jimmy",
#     "animal": "cat",
#     "breed": "shorthair",
#     "age": 2,
#     "health": "good",
#     "neutered": "false"
# }
# # Insert document (row) into the database's collection (table)
# collection_shelter.insert_one(record)
# testing = collection_shelter.find_one()
# print(testing)
# exit()


# delete collection data
# collection_shelter.delete_many({})
# exit()


# Convert the Collection (table) date to a pandas DataFrame for dropdown options
df = pd.DataFrame(list(collection_shelter.find()))
# drop the id column
inputlist = df.iloc[:, 1:]
print(inputlist.head())


layout = html.Div([
    html.H1("Updating Existing Data of Mongo Server on the Cloud"),
    dcc.Dropdown(id='owner-chosen', multi=False, style={'width':"50%"}, placeholder="Select owner",
                 options=[{'label': x, 'value': x} for x in df.owner.unique()]),

    dcc.Dropdown(id="categories", multi=False, style={'width':"50%"}, clearable=False, placeholder="Select category to update",
                 options=[{'label': x, 'value': x} for x in df.columns]),
    dcc.Input(id="input-value", type="text", placeholder="Insert updated info"),
    html.Button("Save to Mongo Server",id='save-to-mongodb'),

    html.Hr(),
    html.P(),
    html.H1("Inserting new Documents (rows) into Mongo Server on the Cloud"),

    html.Div(children=[dcc.Input(id="input-{}".format(x), placeholder="insert {}".format(x))
                       for x in inputlist.columns]),
    html.Button("Insert New Document(row)", id='save-new-row'),

    html.Br(),
    html.Div(id="ownersd-div"),
    html.Div(id='hidden-content'),
])


# Update existing rows
@callback(
    Output("hidden-content", "children"),
    Input("save-to-mongodb","n_clicks"),
    State("owner-chosen", "value"),
    State("categories", "value"),
    State("input-value", "value"),
    prevent_initial_call=True
)
def update_mongodb(n, own_v, categ_v, input_v):
    # more MongoDB commands: https://docs.mongodb.com/manual/reference/command/update/
    collection_shelter.update_one({"owner": own_v}, {"$set": {categ_v: input_v}})
    return ""


# Insert new Documents (rows)
@callback(
    Output("ownersd-div", "children"),
    Input("save-new-row","n_clicks"),
    State("input-owner", "value"),
    State("input-animal", "value"),
    State("input-breed", "value"),
    State("input-health", "value"),
    State("input-age", "value"),
    State("input-neutered", "value"),
    prevent_initial_call=True
)
def new_mongodb_row(n, own_v, anim_v, breed_v, health_v, age, netrd_v):
    collection_shelter.insert_one(
        {
            "owner": own_v,
            "animal": anim_v,
            "breed": breed_v,
            "age": age,
            "health": health_v,
            "neutered": netrd_v
        }
    )

    docs = collection_shelter.find()
    info_list = []
    for doc in docs:
        info_list.append(doc['owner'] + " is owner of a " + doc["animal"]+"...AND...")
    text = html.H3(children=info_list)
    return text
