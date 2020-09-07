import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from datetime import datetime as dt
import npm_stat


def stats_old(data):
    top10_x, top10_y = npm_stat.get_top10(data)
    trends_x, trends_y = npm_stat.get_trends(data)
    fig = go.Figure(data=[go.Scatter(x=trends_x, y=trends_y)], layout={
        "plot_bgcolor": "#F9F9F9",
        "paper_bgcolor": "#F9F9F9",
        'title': 'Downloads trends over time.'})
    return [dcc.Graph(
        id='top10',
        figure={
            'data': [
                {"x": top10_x, "y": top10_y, 'type': 'bar', 'name': 'downloads'}
            ],
            'layout': {
                'title': 'Top 10 downloaded packages.',
                "plot_bgcolor": "#F9F9F9",
                "paper_bgcolor": "#F9F9F9"
            }
        }
    ),
        dcc.Graph(
        id='trends',
        figure=fig
    )
    ]


def header():
    return html.Div(
        [
            html.Div(
                [
                    html.Img(
                        src="/assets/logo.png",
                        id="logo",
                        style={
                            "height": "60px",
                            "width": "auto",
                            "marginBottom": "25px",
                        },
                    )
                ],
                className="one-third column",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H3(
                                "NPM Dashboard",
                                style={"marginBottom": "0px"},
                            ),
                            html.H5(
                                "Dashboard for npm, to get statistics for packages.", style={"marginTop": "0px"}
                            ),
                        ]
                    )
                ],
                className="one-half column",
                id="title",
            ),
            html.Div(
                [
                    html.A(
                        html.Button("Github", id="learn-more-button"),
                        href="https://github.com",
                    )
                ],
                className="one-third column",
                id="button",
            ),
        ],
        id="header",
        className="row flex-display",
        style={"marginBottom": "25px"},
    )


def options():
    return html.Div(id="top-header", children=[
        dcc.Input(
            type="text",
            id='name',
            value='',
            placeholder='Username',
            className="one-third column"
        ),
        dcc.DatePickerRange(
            id='date-picker-range',
            className="one-third column"
        ),
        html.Button(
            'Submit', id='submit-pkg', n_clicks=0,  className=" one-third column")
    ])


def stats(data):
    top10_x, top10_y = npm_stat.get_top10(data)
    trends_x, trends_y = npm_stat.get_trends(data)
    fig = go.Figure(data=[go.Scatter(x=trends_x, y=trends_y)], layout={
        "plot_bgcolor": "#F9F9F9",
        "paper_bgcolor": "#F9F9F9",
        'title': 'Downloads trends over time.'})

    return html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='top10',
                        figure={
                            'data': [
                                {"x": top10_x, "y": top10_y,
                                    'type': 'bar', 'name': 'downloads'}
                            ],
                            'layout': {
                                'title': 'Top 10 downloaded packages.',
                                "plot_bgcolor": "#F9F9F9",
                                "paper_bgcolor": "#F9F9F9"
                            }
                        }
                    )

                ],
                className="pretty_container four columns",
                id="cross-filter-options",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [html.H6("152"),
                                 html.P("Total")],
                                id="total",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H6("20"),
                                 html.P("monthly min")],
                                id="monthly min",
                                className="mini_container",
                            ), html.Div(
                                [html.H6("100"),
                                 html.P("monthly avg")],
                                id="monthly avg",
                                className="mini_container",
                            ), html.Div(
                                [html.H6("152"),
                                 html.P("monthly max")],
                                id="monthly max",
                                className="mini_container",
                            )

                        ],
                        id="info-container",
                        className="row container-display",
                    ),
                    html.Div(
                        [dcc.Graph(
                            id='trends',
                            figure=fig
                        )],
                        id="countGraphContainer",
                        className="pretty_container",
                    ),
                ],
                id="right-column",
                className="eight columns",
            ),
        ],
        className="row flex-display",
    )
