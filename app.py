import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from datetime import datetime as dt
import npm_stat
import components
from flask import send_from_directory
import os

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
        # components.layout(),
        html.Div(id="output", style={'display': 'none'}, children=[
            html.Div(id='display-value'),
            html.Div(id='dates'),
        ]),
        html.Div(id='stats', children='No Data.', style={
            'textAlign': 'center',
        }),
    ])


@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)


@app.callback(
    dash.dependencies.Output('dates', 'children'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        state["start"] = start_date
    if end_date is not None:
        state["end"] = end_date
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix

    return 'Select a date.'


@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('name', 'value')])
def display_name(value):
    state["name"] = value
    return 'You have typed "{}"'.format(value)


def get_view(view_type, value, from_date, until_date):
    if(view_type is None or value is None or from_date is None or until_date is None):
        raise Exception("missing details")
    data = npm_stat.get_downloads(
        view_type, value, from_date, until_date)

    return components.stats(data)


@app.callback(
    dash.dependencies.Output('stats', 'children'),
    [dash.dependencies.Input('submit-pkg', 'n_clicks')],
    [dash.dependencies.State('stats', 'children')])
def update_output(value, old_output):
    if(value > 0):
        return get_view(state["type"], state["name"], state["start"], state["end"])
    elif value > 0:
        return 'Please fill package name first.'


if __name__ == '__main__':
    app.run_server(debug=True)
