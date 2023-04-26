import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd

app = dash.Dash(__name__)

data = {
    "Team": ["Team A", "Team B", "Team C", "Team D"],
    "Goals": [3, 1, 0, 2],
    "Shots on Goal": [5, 3, 2, 4],
    "Possession": ["45%", "35%", "20%", "40%"],
}

df = pd.DataFrame(data)

table_header = [html.Thead(html.Tr([html.Th(col) for col in df.columns]))]

table_body = [
    html.Tbody(
        [
            html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
            for i in range(len(df))
        ]
    )
]

table = html.Table(table_header + table_body)

app.layout = html.Div(children=[table])

if __name__ == "__main__":
    app.run_server(debug=True)  # port='8050'
