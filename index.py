from dash import Input, Output, dcc, html, State
import dash


import dash
import dash_labs as dl  # pip install dash-labs
import dash_bootstrap_components as dbc # pip install dash-bootstrap-components

# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server

import dash_labs as dl  # pip install dash-labs
import dash_bootstrap_components as dbc # pip install dash-bootstrap-components

# Connect to your app pages
# from apps import global_sales, animal_calls, country_population, data_share, datatable, recycling,choro_map, dash_excel, dash_api_data
from pages import crud, mongo_dash_AWS, uploading, vgames
from servers import mongo_crud #dash_bigQuery

# navbar = dbc.NavbarSimple(
#     children=[
#         dbc.DropdownMenu(
#             [
#                 dbc.DropdownMenuItem(page["name"], href=page["path"])
#                 for page in dash.page_registry.values()
#                 if page["module"] != "pages.not_found_404"
#             ],
#             nav=True,
#             label="More Pages",
#         ),
#     ],
#     brand="Multi Page App Plugin Demo",
#     color="primary",
#     dark=True,
#     className="mb-2",
#     fluid=True
# )


offcanvas = html.Div(
    [
        dbc.Button("Menu", id="open-offcanvas", n_clicks=0),
        dbc.Offcanvas(
            dbc.ListGroup(
                [
                    dbc.ListGroupItem(page["name"], href=page["path"])
                    for page in dash.page_registry.values()
                    if page["module"] != "pages.not_found_404"
                ]
            ),
            id="offcanvas",
            is_open=False,
        ),
    ],
    className="my-3"
)


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
#         dcc.Link("CRUD Dash AWS | ",  href='/apps/crud'),
#     ], className="row"),
#     #navbar,
#     offcanvas,
#     html.Div(id='page-content', children=[])
# ])

app.layout = dbc.Container(
    #[navbar, dl.plugins.page_container],
    [offcanvas, dl.plugins.page_container],
    fluid=True,
)

@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


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
#     if pathname == '/apps/crud':
#         return crud.layout
#     else:
#          return dash_api_data.layout


if __name__ == '__main__':
    app.run_server(debug=True)
