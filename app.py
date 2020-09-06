import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from datetime import datetime as dt
import npm_stat

state = {
    "type": "package"
}

app = dash.Dash()

app.layout = html.Div(id='container', children=[
    html.H1(
        children='NPM Dashboard',
        style={
            'textAlign': 'center',
        }
    ),
    html.Div(children='Dashboard for npm, to get statistics on packages.', style={
        'textAlign': 'center',
    }),
    html.Label('Type:'),
    dcc.Dropdown(
        id='type-dropdown',
        options=[
            {'label': 'package', 'value': 'package'},
            {'label': 'author', 'value': 'author'},
        ],
        value='package'
    ),
    html.Div(id='type'),
    html.Label('Package:'),
    html.Br(),
    dcc.Input(
        type="text",
        id='name',
        value='',
        placeholder='react or username'
    ),
    html.Div(id='display-value'),
    dcc.DatePickerRange(
        id='date-picker-range'
    ),
    html.Div(id='dates'),
    html.Button('Submit', id='submit-pkg', n_clicks=0),
    html.Div(id='stats', children=[
        html.Div("No Data.")
    ]),
])


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


@app.callback(dash.dependencies.Output('type', 'children'),
              [dash.dependencies.Input('type-dropdown', 'value')])
def display_type(value):
    state["type"] = value
    return 'Type: {}'.format(value)


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

    top10_x, top10_y = npm_stat.get_top10(data)
    trends_x, trends_y = npm_stat.get_trends(data)

    fig = go.Figure(data=[go.Scatter(x=trends_x, y=trends_y)], layout={
        'title': 'Downloads trends over time.'})

    return [dcc.Graph(
        id='top10',
        figure={
            'data': [
                {"x": top10_x, "y": top10_y, 'type': 'bar', 'name': 'downloads'}
            ],
            'layout': {
                'title': 'Top 10 downloaded packages.'
            }
        }
    ),
        dcc.Graph(
        id='trends',
        figure=fig
    )
    ]


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
