# import pandas as pd 
# import plotly.express as px
# import pathlib
# from dash import dcc
# from dash import html
# from dash.dependencies import Input, Output, State
# from app import app

# #---------------------------------------------------------------
# # get relative data folder
# PATH = pathlib.Path(__file__).parent
# # DATA_PATH = PATH.joinpath("../datasets").resolve()


# # df = pd.read_csv(DATA_PATH.joinpath("DOHMH_New_York_City_Restaurant_Inspection_Results.csv"))  # https://drive.google.com/file/d/1jyvSiRjaNIeOCP59dUFQuZ0_N_StiQOr/view?usp=sharing


# df['INSPECTION DATE'] = pd.to_datetime(df['INSPECTION DATE'])
# df = df.groupby(['INSPECTION DATE','CUISINE DESCRIPTION','CAMIS'], as_index=False)['SCORE'].mean()
# df = df.set_index('INSPECTION DATE')
# df = df.loc['2016-01-01':'2019-12-31']
# df = df.groupby([pd.Grouper(freq="M"),'CUISINE DESCRIPTION'])['SCORE'].mean().reset_index()
# # print (df[:5])

# #---------------------------------------------------------------
# layout = html.Div([

#     html.Div([
#         dcc.Graph(id='restaurant_inspection_graph')
#     ],className='nine columns'),

#     html.Div([

#         html.Br(),
#         html.Label(['Choose 3 Cuisines to Compare:'],style={'font-weight': 'bold', "text-align": "center"}),
#         dcc.Dropdown(id='cuisine_one',
#             options=[{'label':x, 'value':x} for x in df.sort_values('CUISINE DESCRIPTION')['CUISINE DESCRIPTION'].unique()],
#             value='African',
#             multi=False,
#             disabled=False,
#             clearable=True,
#             searchable=True,
#             placeholder='Choose Cuisine...',
#             className='form-dropdown',
#             style={'width':"90%"},
#             persistence='string',
#             persistence_type='memory'),

#         dcc.Dropdown(id='cuisine_two',
#             options=[{'label':x, 'value':x} for x in df.sort_values('CUISINE DESCRIPTION')['CUISINE DESCRIPTION'].unique()],
#             value='Asian',
#             multi=False,
#             clearable=False,
#             persistence='string',
#             persistence_type='session'),

#         dcc.Dropdown(id='cuisine_three',
#             options=[{'label':x, 'value':x} for x in df.sort_values('CUISINE DESCRIPTION')['CUISINE DESCRIPTION'].unique()],
#             value='Donuts',
#             multi=False,
#             clearable=False,
#             persistence='string',
#             persistence_type='local'),

#     ],className='three columns'),

# ])

# #---------------------------------------------------------------

# @app.callback(
#     Output('restaurant_inspection_graph','figure'),
#     [Input('cuisine_one','value'),
#      Input('cuisine_two','value'),
#      Input('cuisine_three','value')]
# )

# def build_graph(first_cuisine, second_cuisine, third_cuisine):
#     dff=df[(df['CUISINE DESCRIPTION']==first_cuisine)|
#            (df['CUISINE DESCRIPTION']==second_cuisine)|
#            (df['CUISINE DESCRIPTION']==third_cuisine)]
#     # print(dff[:5])

#     fig = px.line(dff, x="INSPECTION DATE", y="SCORE", color='CUISINE DESCRIPTION', height=600)
#     fig.update_layout(yaxis={'title':'NEGATIVE POINT'},
#                       title={'text':'Restaurant Inspections in NYC',
#                       'font':{'size':28},'x':0.5,'xanchor':'center'})
#     return fig

# #---------------------------------------------------------------

    
    
# # https://youtu.be/Kr94sFOWUMg
