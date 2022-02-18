from dash import Dash, html, dcc, Input, Output
import altair as alt
import pandas as pd


data = pd.read_csv("data/Preprocessed_data.csv")

carriers = data["carrier_name"].unique()
def plot_altair(carrier_name):
    plot = data.loc[data["carrier_name"].isin(carrier_name),:]
    chart = alt.Chart(plot).mark_line(size=3).encode(
         alt.X("month", title = "Month"),
         alt.Y("percent_cancelled", title = "Percent of Flights Cancelled"),
         color = alt.Color("carrier_name", title = "Carrier Name")
    )
    return chart.to_html()

app = Dash(__name__)
server = app.server
app.title = "Flight Cancellations 2019"

app.layout = html.Div([
    html.H2(style={
            'textAlign': 'center',
        }, children='Flight Canellations 2019'),
    dcc.Dropdown(
            id='carrier_name', 
            value=["Alaska Airlines Inc."],
            options=[{'label': i, 'value': i} for i in carriers],
            multi=True),
    html.Iframe( id = "line_plot",
        style={'border-width': '0', 'width': '100%', 'height': '600px'},
        srcDoc= plot_altair(["Alaska Airlines Inc."]))])

@app.callback(
    Output('line_plot', 'srcDoc'),
    Input('carrier_name', 'value'))

def update_output(carrier_name):
    return plot_altair(carrier_name)

if __name__ == '__main__':
    app.run_server(debug=True)