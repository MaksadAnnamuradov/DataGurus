import pandas as pd
import plotly.express as px
import pathlib
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("Urban_Park_Ranger_Animal_Condition.csv"))

#---------------------------------------------------------------
animal_layout = html.Div([

    html.Div([
        dcc.Graph(id='animal_rescue_graph')
    ],className='nine columns'),

    html.Div([

        html.Br(),
        html.Div(id='output_data'),
        html.Br(),

        html.Label(['Choose column:'],style={'font-weight': 'bold', "text-align": "center"}),

        dcc.Dropdown(id='my_dropdown',
            options=[
                     {'label': 'Species', 'value': 'Animal Class'},
                     {'label': 'Final Ranger Action', 'value': 'Final Ranger Action'},
                     {'label': 'Age', 'value': 'Age', 'disabled':True},
                     {'label': 'Animal Condition', 'value': 'Animal Condition'},
                     {'label': 'Borough', 'value': 'Borough'},
                     {'label': 'Species Status', 'value': 'Species Status'}
            ],
            optionHeight=35,                    #height/space between dropdown options
            value='Borough',                    #dropdown value selected automatically when page loads
            disabled=False,                     #disable dropdown value selection
            multi=False,                        #allow multiple dropdown values to be selected
            searchable=True,                    #allow user-searching of dropdown values
            search_value='',                    #remembers the value searched in dropdown
            placeholder='Please select...',     #gray, default text shown when no option is selected
            clearable=True,                     #allow user to removes the selected value
            style={'width':"100%"},             #use dictionary to define CSS styles of your dropdown
            className='select_box',           #activate separate CSS document in assets folder
            # persistence=True,                 #remembers dropdown value. Used with persistence_type
            # persistence_type='memory'         #remembers dropdown value selected until...
            ),                                  #'memory': browser tab is refreshed
                                                #'session': browser tab is closed
                                                #'local': browser cookies are deleted
    ],className='three columns'),

])