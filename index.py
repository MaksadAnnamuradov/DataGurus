from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import vgames, global_sales, animal_calls, country_population, uploading, data_share, datatable, recycling, choro_map


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Video Games| ', href='/apps/vgames'),
        # dcc.Link('Other Products| ', href='/apps/global_sales'),
        # dcc.Link('Animal Calls| ', href='/apps/animal_calls'),
        #dcc.Link('Restaurant Inspections| ', href='/apps/restaurant_inspections'),
        dcc.Link('Country Population|', href='/apps/country_population'),
        dcc.Link('Uploading Data| ', href='/apps/uploading'),
        # dcc.Link('Sharing Data| ', href='/apps/data_share'),
        dcc.Link('Data Table| ', href='/apps/datatable'),
        dcc.Link("Recycling|",  href='/apps/recycling'),
         dcc.Link("choroMap",  href='/apps/choro_map'),
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
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=True)
