import dash

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__)
app.scripts.config.serve_locally = True

app.layout = html.Div([
    html.Button('OUTPUT', id='output-btn'),

    html.Table([
        html.Thead([
            html.Tr([
                html.Th('Output 1'),
                html.Th('Output 2')
            ])
        ]),
        html.Tbody([
            html.Tr([html.Td(id='output1'), html.Td(id='output2')]),
        ])
    ]),
])


@app.callback([Output('output1', 'children'), Output('output2', 'children')],
              [Input('output-btn', 'n_clicks')],
              [State('output-btn', 'n_clicks_timestamp')])
def on_click(n_clicks, n_clicks_timestamp):
    if n_clicks is None:
        raise PreventUpdate

    return n_clicks, n_clicks_timestamp


if __name__ == '__main__':
    app.run_server(debug=True,host ='0.0.0.0', port=6060)