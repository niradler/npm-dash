import dash
import dash_core_components as dcc
import dash_html_components as html
from flask import send_from_directory
import os
import json
import npm_stat
import components

state = {
    "type": "author"
}

app = dash.Dash()

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app.layout = html.Div(
    id="mainContainer", style={
        "display": "flex",
        "flexDirection": "column"
    }, children=[
        html.Link(
            rel='stylesheet',
            href='/assets/plotly.css'
        ),
        html.Link(
            rel='stylesheet',
            href='/assets/style.css'
        ),
        components.header(),
        components.options(),
        html.Div(id="output", style={'display': 'none'}, children=[
            html.Div(id='name-value'),
            html.Div(id='dates'),
        ]),
        dcc.Loading(
            id="loading",
            type="default",
            style={
                'marginTop': '5%'
            },
            children=html.Div(id='stats', children=[html.Div(id='data-container', children='No Data.', style={
                'textAlign': 'center',
                'marginTop': '5%'
            })]))

    ])


@ app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)


@ app.callback(
    dash.dependencies.Output('dates', 'children'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])
def update_output(start_date, end_date):

    return json.dumps({"start_date": start_date, "end_date": end_date})


@ app.callback(dash.dependencies.Output('name-value', 'children'),
               [dash.dependencies.Input('name', 'value')])
def display_name(value):
    return value


def get_view(view_type, value, from_date, until_date):
    if(view_type is None or value is None or from_date is None or until_date is None):
        raise Exception("missing details")
    data = npm_stat.get_downloads(
        view_type, value, from_date, until_date)

    return components.stats(data)


@ app.callback(
    dash.dependencies.Output('stats', 'children'),
    [dash.dependencies.Input('submit-pkg', 'n_clicks'), dash.dependencies.Input('name', 'value'), dash.dependencies.Input(
        'date-picker-range', 'start_date'), dash.dependencies.Input('date-picker-range', 'end_date')]
)
def update_output(clicks, name, start_date, end_date):
    print(clicks, name, start_date, end_date)
    if(clicks > 0):
        return get_view(state["type"],  name, start_date, end_date)
    elif clicks > 0:
        return 'Please fill package name first.'


if __name__ == '__main__':
    app.run_server(debug=True)
