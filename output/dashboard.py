import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd

app = dash.Dash(__name__)

data = {
    "Команда": ["ЦСКА", "Зенит"],
    "Голы": [3, 1],
    "Голевые передачи": [5, 3],
    "Владение": ["65%", "35%"],
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
