from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

from scripts.database_init import create_database_if_not_exist, create_tables, fetch_data
# Create the database and tables if they do not exist
create_database_if_not_exist()
create_tables()

# Create the Dash application
app = Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])

# Define custom CSS styles
custom_styles = {
    'backgroundColor':'white',  
    'color': '#DE1010',  # Bright red text color
    'margin-left': '0', 
    'margin-right': '0', 
    "font-style": "italic"
    #'font-weight': 'bold' 
}

# Define the layout
app.layout = html.Div(
    style=custom_styles,  # Apply custom styles to the entire app
    children=[
        dbc.Container(
            children=[
                dbc.Row(
                    dbc.Col(
                        html.H1(
                            children="Bixi Availability : Montreal Live Map",
                            className="p-2 mb-2 text-center",
                            style={"font-size": "50px", "width": "100%", "top": "0", "z-index": "999", "font-style": "italic",'background-color': '#DE1010', 'padding': '10px', 'color': 'white'}
                        )
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            children="Number of users currently riding Bixi bikes:",
                            className="text-center",
                              
                        )
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            id="bixi-not-parked",
                            className="text-center"
                        )
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            children="Last update : ",
                            className="text-center",
                            
                        )
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            id="last-update",
                            className="text-center"
                        )
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(
                            id="bixi-map",
                            style={"height": "800px", "width": "100%"},
                            config={'displayModeBar': False},  # Hide the mode bar
                            figure={
                                'layout': go.Layout(
                                    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
                                    plot_bgcolor='rgba(0,0,0,0)'  # Transparent plot area background
                                )
                            }
                        )
                    )
                ),
                dcc.Interval(
                    id="data-refresh-interval",
                    interval=10000,  # Refresh the data every 10 seconds (adjust as needed)
                    n_intervals=0
                )
            ]
        )
    ]
)


# Callback to update the data periodically
@app.callback(
    [
        Output("bixi-not-parked", "children"),
        Output("last-update", "children"),
        Output("bixi-map", "figure")
    ],
    Input("data-refresh-interval", "n_intervals")
)
def update_data(n):
    # Fetch the latest data from the database (includes airflow updates)
    df = fetch_data()
    print(df.shape)

    # Compute amount of bixi not parked
    bixi_not_parked = np.sum(df["capacity"] - df["num_docks_available"])

    # transforming UTC datetime to Montreal based hours
    df["last_reported"] = pd.to_datetime(df['last_reported'], unit='s', utc=True).dt.tz_convert("America/Montreal")

    # Get the last update time
    last_update = df["last_reported"].max().strftime("%H:%M %d/%m/%Y")

    # Generate the map figure
    # Add number of e-bikes available
    # Generate the map figure
    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        color=df["num_bikes_available"] + df["num_ebikes_available"],  # Color based on total bikes available
        size="capacity",
        color_continuous_scale="bluered",
        size_max=15,
        zoom=10,
        hover_name="name",
        custom_data=["name", "capacity", "num_bikes_available", "num_ebikes_available"]
    )
    fig.update_layout(mapbox_style="open-street-map")

    # fig = px.scatter_mapbox(
    #     df,
    #     lat="lat",
    #     lon="lon",
    #     color="num_bikes_available",
    #     size="capacity",
    #     color_continuous_scale="haline",
    #     size_max=15,
    #     zoom=10,
    #     hover_name="name",
    #     custom_data=["name", "capacity", "num_bikes_available"]
    # )
    # fig.update_layout(mapbox_style="open-street-map")

    return bixi_not_parked, last_update, fig


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)

