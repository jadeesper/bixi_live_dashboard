from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

from scripts.database_init import create_database_if_not_exist, create_tables, fetch_data
# Create the database and tables if they do not exist
create_database_if_not_exist()
create_tables()

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# Define the layout
app.layout = html.Div(
    children=[
        html.H1(
            children="Bixi station map",
            style={
                "font_family": "cursive",
                "textAlign": "center"
            }
        ),
        html.Div(
            children="Number of bixi bikes not parked",
            style={
                "font_family": "cursive",
                "textAlign": "center"
            }
        ),
        html.Div(
            id="bixi-not-parked",
            style={
                "font_family": "cursive",
                "textAlign": "center"
            }
        ),
        html.Div(
            children="Last update : ",
            style={
                "font_family": "cursive",
                "textAlign": "center"
            }
        ),
        html.Div(
            id="last-update",
            style={
                "font_family": "cursive",
                "textAlign": "center"
            }
        ),
        dcc.Graph(id="bixi-map", style={"height": "800px", "width": "100%"}),
        dcc.Interval(
            id="data-refresh-interval",
            interval=10000,  # Refresh the data every 10 seconds (adjust as needed)
            n_intervals=0
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
    # fig = px.scatter_mapbox(
    #     df,
    #     lat="lat",
    #     lon="lon",
    #     color=df["num_bikes_available"] + df["num_ebikes_available"],  # Color based on total bikes available
    #     size="capacity",
    #     color_continuous_scale="haline",
    #     size_max=15,
    #     zoom=10,
    #     hover_name="name",
    #     custom_data=["name", "capacity", "num_bikes_available", "num_ebikes_available"]
    # )
    # fig.update_layout(mapbox_style="open-street-map")

    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        color="num_bikes_available",
        size="capacity",
        color_continuous_scale="haline",
        size_max=15,
        zoom=10,
        hover_name="name",
        custom_data=["name", "capacity", "num_bikes_available"]
    )
    fig.update_layout(mapbox_style="open-street-map")

    return bixi_not_parked, last_update, fig


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
