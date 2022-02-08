# from dash import Input, Output, dcc, html

# # Connect to main app.py file
# from app import app
# from app import server

# # Connect to your app pages
# from apps import vgames, global_sales, animal_calls, country_population, uploading, data_share, datatable, recycling,choro_map, dash_excel, dash_api_data, mongo_dash_AWS #dash_bigQuery


# app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     html.Div([
#         dcc.Link('Historgrams | ', href='/apps/vgames'),
#         # dcc.Link('Other Products| ', href='/apps/global_sales'),
#         # dcc.Link('Animal Calls| ', href='/apps/animal_calls'),
#         #dcc.Link('Restaurant Inspections| ', href='/apps/restaurant_inspections'),
#         dcc.Link('Line Graphs | ', href='/apps/country_population'),
#         dcc.Link('Data Upload | ', href='/apps/uploading'),
#         # dcc.Link('Sharing Data| ', href='/apps/data_share'),
#         dcc.Link('Data Table | ', href='/apps/datatable'),
#         dcc.Link("Data Map | ",  href='/apps/recycling'),
#         dcc.Link("Chloro Map | ",  href='/apps/choro_map'),
#         # dcc.Link("Dash Excel | ",  href='/apps/dash_excel'),
#         dcc.Link("Dash API Data | ",  href='/apps/dash_api_data'),
#         dcc.Link("MongoDB Dash AWS | ",  href='/apps/mongo_dash_AWS'),
#         # dcc.Link("BigQuery Dash AWS | ",  href='/apps/dash_bigQuery'),
#     ], className="row"),
#     html.Div(id='page-content', children=[])
# ])


# @app.callback(Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/apps/vgames':
#         return vgames.layout
#     # if pathname == '/apps/global_sales':
#     #     return global_sales.layout
#     # if pathname == '/apps/animal_calls':
#     #     return animal_calls.layout
#     # if pathname == '/apps/restaurant_inspections':
#     #     return restaurant_inspections.layout
#     if pathname == '/apps/country_population':
#         return country_population.layout
#     if pathname == '/apps/uploading':
#         return uploading.layout
#     # if pathname == '/apps/data_share':
#     #     return data_share.layout
#     if pathname == '/apps/datatable':
#         return datatable.layout
#     if pathname == '/apps/recycling':
#         return recycling.layout
#     if pathname == '/apps/choro_map':
#         return choro_map.layout
#     # if pathname == '/apps/dash_excel':
#     #     return dash_excel.layout
#     if pathname == '/apps/dash_api_data':
#         return dash_api_data.layout
#     if pathname == '/apps/mongo_dash_AWS':
#         return mongo_dash_AWS.layout
#     # if pathname == '/apps/dash_bigQuery':
#     #     return dash_bigQuery.layout
#     else:
#          return dash_api_data.layout


# if __name__ == '__main__':
#     app.run_server(debug=True)



import dash
from dash import Input, Output, State, dcc, html
from sqlalchemy import Table, create_engine
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import warnings
import os
from flask_login import login_user, logout_user, current_user, LoginManager, UserMixin
import configparser


warnings.filterwarnings("ignore")
conn = sqlite3.connect('data.sqlite')
engine = create_engine('sqlite:///data.sqlite')
db = SQLAlchemy()
config = configparser.ConfigParser()
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable = False)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
Users_tbl = Table('users', Users.metadata)

app = dash.Dash(__name__)

server = app.server

app.config.suppress_callback_exceptions = True

# config
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI='sqlite:///data.sqlite',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db.init_app(server)
# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'
#User as base
# Create User class with UserMixin
class Users(UserMixin, Users):
    pass
create = html.Div([ html.H1('Create User Account')
        , dcc.Location(id='create_user', refresh=True)
        , dcc.Input(id="username"
            , type="text"
            , placeholder="user name"
            , maxLength =15)
        , dcc.Input(id="password"
            , type="password"
            , placeholder="password")
        , dcc.Input(id="email"
            , type="email"
            , placeholder="email"
            , maxLength = 50)
        , html.Button('Create User', id='submit-val', n_clicks=0)
        , html.Div(id='container-button-basic')
    ])
    #end div
login =  html.Div([dcc.Location(id='url_login', refresh=True)
            , html.H2('''Please log in to continue:''', id='h1')
            , dcc.Input(placeholder='Enter your username',
                    type='text',
                    id='uname-box')
            , dcc.Input(placeholder='Enter your password',
                    type='password',
                    id='pwd-box')
            , html.Button(children='Login',
                    n_clicks=0,
                    type='submit',
                    id='login-button')
            , html.Div(children='', id='output-state')
        ]) #end div
success = html.Div([dcc.Location(id='url_login_success', refresh=True)
            , html.Div([html.H2('Login successful.')
                    , html.Br()
                    , html.P('Select a Dataset')
                    , dcc.Link('Data', href = '/data')
                ]) #end div
            , html.Div([html.Br()
                    , html.Button(id='back-button', children='Go back', n_clicks=0)
                ]) #end div
        ]) #end div
data = html.Div([dcc.Dropdown(
                    id='dropdown',
                    options=[{'label': i, 'value': i} for i in ['Day 1', 'Day 2']],
                    value='Day 1')
                , html.Br()
                , html.Div([dcc.Graph(id='graph')])
            ]) #end div
failed = html.Div([ dcc.Location(id='url_login_df', refresh=True)
            , html.Div([html.H2('Log in Failed. Please try again.')
                    , html.Br()
                    , html.Div([login])
                    , html.Br()
                    , html.Button(id='back-button', children='Go back', n_clicks=0)
                ]) #end div
        ]) #end div
logout = html.Div([dcc.Location(id='logout', refresh=True)
        , html.Br()
        , html.Div(html.H2('You have been logged out - Please login'))
        , html.Br()
        , html.Div([login])
        , html.Button(id='back-button', children='Go back', n_clicks=0)
    ])#end div
app.layout= html.Div([
            html.Div(id='page-content', className='content')
            ,  dcc.Location(id='url', refresh=False)
        ])
# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
@app.callback(
    Output('page-content', 'children')
    , [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return create
    elif pathname == '/login':
        return login
    elif pathname == '/success':
        if current_user.is_authenticated:
            return success
        else:
            return failed
    elif pathname =='/data':
        if current_user.is_authenticated:
            return data
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return logout
        else:
            return logout
    else:
        return '404'
#set the callback for the dropdown interactivity
@app.callback(
    [Output('graph', 'figure')]
    , [Input('dropdown', 'value')])
def update_graph(dropdown_value):
    if dropdown_value == 'Day 1':
        return [{'layout': {'title': 'Graph of Day 1'}
                , 'data': [{'x': [1, 2, 3, 4]
                    , 'y': [4, 1, 2, 1]}]}]
    else:
        return [{'layout': {'title': 'Graph of Day 2'}
                ,'data': [{'x': [1, 2, 3, 4]
                    , 'y': [2, 3, 2, 4]}]}]
@app.callback(
   [Output('container-button-basic', "children")]
    , [Input('submit-val', 'n_clicks')]
    , [State('username', 'value'), State('password', 'value'), State('email', 'value')])

def insert_users(n_clicks, un, pw, em):
    hashed_password = generate_password_hash(pw, method='sha256')

    if un is not None and pw is not None and em is not None:
        ins = Users_tbl.insert().values(username=un,  password=hashed_password, email=em,)
        conn = engine.connect()
        conn.execute(ins)
        conn.close()
        return [login]
    else:
        return [html.Div([html.H2('Already have a user account?'), dcc.Link('Click here to Log In', href='/login')])]
@app.callback(
    Output('url_login', 'pathname')
    , [Input('login-button', 'n_clicks')]
    , [State('uname-box', 'value'), State('pwd-box', 'value')])
def successful(n_clicks, input1, input2):
    user = Users.query.filter_by(username=input1).first()
    if user:
        if check_password_hash(user.password, input2):
            login_user(user)
            return '/success'
        else:
            pass
    else:
        pass
@app.callback(
    Output('output-state', 'children')
    , [Input('login-button', 'n_clicks')]
    , [State('uname-box', 'value'), State('pwd-box', 'value')])
def update_output(n_clicks, input1, input2):
    if n_clicks > 0:
        user = Users.query.filter_by(username=input1).first()
        if user:
            if check_password_hash(user.password, input2):
                return ''
            else:
                return 'Incorrect username or password'
        else:
            return 'Incorrect username or password'
    else:
        return ''
@app.callback(
    Output('url_login_success', 'pathname')
    , [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return '/'
@app.callback(
    Output('url_login_df', 'pathname')
    , [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return '/'
# Create callbacks
@app.callback(
    Output('url_logout', 'pathname')
    , [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return '/'
if __name__ == '__main__':
    app.run_server(debug=True)