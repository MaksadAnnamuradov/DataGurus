from dash import Input, Output, dcc, html

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import vgames, global_sales, animal_calls, country_population, uploading, data_share, datatable, recycling,choro_map, dash_excel, dash_api_data, mongo_dash_AWS, crud #dash_bigQuery


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Historgrams | ', href='/apps/vgames'),
        # dcc.Link('Other Products| ', href='/apps/global_sales'),
        # dcc.Link('Animal Calls| ', href='/apps/animal_calls'),
        #dcc.Link('Restaurant Inspections| ', href='/apps/restaurant_inspections'),
        dcc.Link('Line Graphs | ', href='/apps/country_population'),
        dcc.Link('Data Upload | ', href='/apps/uploading'),
        # dcc.Link('Sharing Data| ', href='/apps/data_share'),
        dcc.Link('Data Table | ', href='/apps/datatable'),
        dcc.Link("Data Map | ",  href='/apps/recycling'),
        dcc.Link("Chloro Map | ",  href='/apps/choro_map'),
        # dcc.Link("Dash Excel | ",  href='/apps/dash_excel'),
        dcc.Link("Dash API Data | ",  href='/apps/dash_api_data'),
        dcc.Link("MongoDB Dash AWS | ",  href='/apps/mongo_dash_AWS'),
        # dcc.Link("BigQuery Dash AWS | ",  href='/apps/dash_bigQuery'),
        dcc.Link("CRUD Dash AWS | ",  href='/apps/crud'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/vgames':
        return vgames.layout
    # if pathname == '/apps/global_sales':
    #     return global_sales.layout
    # if pathname == '/apps/animal_calls':
    #     return animal_calls.layout
    # if pathname == '/apps/restaurant_inspections':
    #     return restaurant_inspections.layout
    if pathname == '/apps/country_population':
        return country_population.layout
    if pathname == '/apps/uploading':
        return uploading.layout
    # if pathname == '/apps/data_share':
    #     return data_share.layout
    if pathname == '/apps/datatable':
        return datatable.layout
    if pathname == '/apps/recycling':
        return recycling.layout
    if pathname == '/apps/choro_map':
        return choro_map.layout
    # if pathname == '/apps/dash_excel':
    #     return dash_excel.layout
    if pathname == '/apps/dash_api_data':
        return dash_api_data.layout
    if pathname == '/apps/mongo_dash_AWS':
        return mongo_dash_AWS.layout
    # if pathname == '/apps/dash_bigQuery':
    #     return dash_bigQuery.layout
    if pathname == '/apps/crud':
        return crud.layout
    else:
         return dash_api_data.layout


if __name__ == '__main__':
    app.run_server(debug=True)
