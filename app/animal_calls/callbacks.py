import pandas as pd
import plotly.express as px
import pathlib
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


#---------------------------------------------------------------
#Taken from https://opendata.cityofnewyork.us/
# df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Dash%20Components/Dropdown/Urban_Park_Ranger_Animal_Condition.csv")  


# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("Urban_Park_Ranger_Animal_Condition.csv"))



def register_animal_callbacks(app):

    #---------------------------------------------------------------
    # Connecting the Dropdown values to the graph
    @app.callback(
        Output(component_id='animal_rescue_graph', component_property='figure'),
        [Input(component_id='my_dropdown', component_property='value')]
    )

    def build_graph(column_chosen):
        dff=df
        fig = px.pie(dff,names=column_chosen)
        fig.update_traces(textinfo='percent+label')
        fig.update_layout(title={'text':'NYC Calls for Animal Rescue',
                        'font':{'size':28},'x':0.5,'xanchor':'center'})
        return fig

    #---------------------------------------------------------------
    # For tutorial purposes to show the user the search_value

    @app.callback(
        Output(component_id='output_data', component_property='children'),
        [Input(component_id='my_dropdown', component_property='search_value')]
    )

    def build_graph(data_chosen):
        return ('Search value was: " {} "'.format(data_chosen))
    #---------------------------------------------------------------

