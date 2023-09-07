import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.read_csv('monitoring_stations_PL.csv')

app = dash.Dash(__name__)
server=app.server
app.layout = html.Div([
    html.H1('Map of Monitoring Stations'),

    dcc.Dropdown(
        id='param-dropdown',
        options=[
            {'label': 'NO2', 'value': 'NO2'},
            {'label': 'O3', 'value': 'O3'},
            {'label': 'C6H6', 'value': 'C6H6'},
            {'label': 'PM10', 'value': 'PM10'},
            {'label': 'PM2.5', 'value': 'PM2.5'},
            {'label': 'CO', 'value': 'CO'},
            {'label': 'SO2', 'value': 'SO2'}
        ],
        multi=False,
        value='NO2'
    ),

    dcc.Graph(id='map-graph',
              style={'width': '100vw', 'height': '100vh'}, config={'scrollZoom': False}),

])

color_palette = {
    'NO2': 'red',
    'O3': 'blue',
    'C6H6': 'green',
    'PM10': 'orange',
    'PM2.5': 'purple',
    'CO': 'black',
    'SO2': 'brown'
}


def create_map(selected_param):
    filtered_df = df[df['pollutant_code'] == selected_param]
    fig = px.scatter_geo(
        filtered_df,
        lat='latitude',
        lon='longitude',
        color='pollutant_code',
        hover_name='station_name',
        projection='natural earth',
        scope='europe'
    )
    fig.update_traces(marker=dict(color=color_palette[selected_param]))
    fig.update_traces(textfont=dict(color='rgba(0, 0, 0, 0)'))
    fig.update_geos(showcoastlines=True, coastlinecolor="black", showland=True, landcolor="white", showocean=True,
                    oceancolor="LightBlue")

    fig.update_geos(
        lonaxis=dict(
            range=[12, 26],
        ),
        lataxis=dict(
            range=[46, 58],
        ),
    )

    return fig


@app.callback(
    Output('map-graph', 'figure'),
    Input('param-dropdown', 'value')
)
def update_map(selected_param):
    updated_fig = create_map(selected_param)
    return updated_fig


if __name__ == '__main__':
    app.run_server(debug=False)
