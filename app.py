import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table_experiments as dt
import re
from datetime import date, datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_table
from dash_extensions import Download

from data import *

####
color_s = "#30aeb0"
filters_list = ["coordinates","type","gender","priority","hospital"]

def make_item(i):
    # we use this function to make the example items to avoid code duplication
    return dbc.Card(
        [
            dbc.CardHeader(
                dbc.Row([
                html.H5(f"{i}".capitalize()),
                daq.BooleanSwitch(
                                id=f"group-{i}-toggle",
                                color=color_s,
                                on=False,
                                style={"border-color":color_s, "align-content":"right"},
                                ),
                ])
            ),
            dbc.Collapse(
                dbc.CardBody(f"This is the content of group {i}..."),
                id=f"collapse-{i}",
            ),
        ]
    )

####

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "3_test"

app.layout = html.Div([
    
    html.Div(
    [
        dbc.Row(
            [
            dbc.Col(
                html.H6("EMERGENCY", style={"font-size":"10pt",
                                            "color":"white",
                                            "backgroundColor":color_s,
                                            "padding-top":"5px",
                                            "padding-bottom":"5px",
                                            "margin-top":"-5px",
                                            "margin-bottom":"0px",
                                            "padding-left":"15px"}),
                ),
            ],
            align="start",
        ),
        dbc.Row(
            [
            dbc.Col(
                [
                html.H6(html.B("LAST 7 DAYS"), style={"font-size":"10pt","padding-left":"15px"}),
                dcc.DatePickerRange(
                            id='my-date-picker-range',
                            calendar_orientation='horizontal',
                            day_size=40,
                            with_portal=False,
                            first_day_of_week=0,
                            clearable=True,
                            number_of_months_shown=2,
                            display_format='MMMM D, YYYY',
                            min_date_allowed=min(df.index).date(),
                            max_date_allowed=max(df.index).date(),
                            initial_visible_month=date(2019,12,27),#max(df.index).date(),
                            start_date=date(2019,12,27),
                            end_date=date(2020,1,2),
                            start_date_placeholder_text="Fisrt Emergence",
                            end_date_placeholder_text="Last Emergence",
                        ),  
                ],
                align="start",
                width=8,
                style={"color":color_s}
            ),
            dbc.Col(
                [
                dbc.Button(
                    html.Center(
                    [
                    html.Img(src='assets/Filters.svg', style={'height':'40%', 'width':'40%', "position":"relative","margin":"auto"}),
                    html.Div(html.B("ADD FILTERS"), style={"color":color_s}),
                    ],
                    ),
                    id="filter-button",
                    color=None
                ),
                dbc.Popover(
                    [
                    dbc.PopoverHeader(
                        [
                        html.B("FILTERS",style={"margin":"auto 0 auto 0"}),
                        dbc.Button(
                            html.Img(src='assets/clear.svg', style={'height':'100%', 'width':'100%', "position":"relative","margin":"auto"}),
                            color=None,
                            id="filter-clear",
                        )
                        ],
                        style={"color":"white","backgroundColor":color_s,"display":"flex","justify-content":"space-between"}
                    ),
                    dbc.PopoverBody(
                        html.Div(
                            [#[make_item(i) for i in filters_list], 
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        dbc.Row([
                                        html.B("Coordinates"),
                                        daq.BooleanSwitch(
                                                        id="group-coordinates-toggle",
                                                        color=color_s,
                                                        on=False,
                                                        style={"border-color":color_s, "align-content":"right"},
                                                        ),
                                        ])
                                    ),
                                    dbc.Collapse(
                                        dbc.CardBody(
                                            [
                                            dbc.Row(
                                                [
                                                dbc.InputGroup(
                                                    [
                                                        dbc.InputGroupAddon("🗺", addon_type="prepend"),
                                                        dbc.Input(placeholder="MIN LAT"),
                                                    ],
                                                    className="mb-3",
                                                    ),
                                                dbc.InputGroup(
                                                    [
                                                        dbc.Input(placeholder="MIN LON"),
                                                        dbc.InputGroupAddon("🗺", addon_type="append"),
                                                    ],
                                                    className="mb-3",
                                                    ),
                                                ],
                                            ),
                                            dbc.Row(
                                                [
                                                dbc.InputGroup(
                                                    [
                                                        dbc.InputGroupAddon("🗺", addon_type="prepend"),
                                                        dbc.Input(placeholder="MAX LAT"),
                                                    ],
                                                    className="mb-3",
                                                    ),
                                                dbc.InputGroup(
                                                    [
                                                        dbc.Input(placeholder="MAX LON"),
                                                        dbc.InputGroupAddon("🗺", addon_type="append"),
                                                    ],
                                                    className="mb-3",
                                                    ),
                                                ],
                                                ),
                                                ]),
                                        id=f"collapse-coordinates",
                                    ),
                                ]
                            ),
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        dbc.Row([
                                        html.B("Type"),
                                        daq.BooleanSwitch(
                                                        id="group-type-toggle",
                                                        color=color_s,
                                                        on=False,
                                                        style={"border-color":color_s, "align-content":"right"},
                                                        className="switch",
                                                        ),
                                        ])
                                    ),
                                    dbc.Collapse(
                                        dbc.CardBody(
                                            dbc.Checklist(
                                                id="checklist-selected-style",
                                                options=[
                                                    {"label": "Type 1", "value": 1},
                                                    {"label": "Type 2", "value": 2},
                                                    {"label": "Type 3", "value": 3},
                                                    {"label": "Type 4", "value": 4},
                                                ],
                                                labelCheckedStyle={"color": color_s},
                                                inline=True,
                                            )
                                            ),
                                        id=f"collapse-type",
                                    ),
                                ]
                            ),
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        dbc.Row([
                                        html.B("Gender"),
                                        daq.BooleanSwitch(
                                                        id="group-gender-toggle",
                                                        color=color_s,
                                                        on=False,
                                                        style={"border-color":color_s, "align-content":"right"},
                                                        ),
                                        ])
                                    ),
                                    dbc.Collapse(
                                        dbc.CardBody(
                                            dbc.RadioItems(
                                                options=[
                                                    {"label": "Male", "value": "male"},
                                                    {"label": "Female", "value": "female"},
                                                ],
                                                value="male",
                                                id="group-gender-items",
                                                inline=True,
                                            ),
                                        ),
                                        id=f"collapse-gender",
                                    ),
                                ]
                            ),
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        dbc.Row([
                                        html.B("Priority"),
                                        daq.BooleanSwitch(
                                                        id="checklist-priority-toggle",
                                                        color=color_s,
                                                        on=False,
                                                        style={"border-color":color_s, "align-content":"right"},
                                                        ),
                                        ])
                                    ),
                                    dbc.Collapse(
                                        dbc.CardBody(
                                            dbc.Checklist(
                                                options=[
                                                    {"label": "Priority 1", "value": "1"},
                                                    {"label": "Priority 2", "value": "2"},
                                                    {"label": "Priority 3", "value": "3"},
                                                ],
                                                value="2",
                                                id="radioitems-inline-input",
                                                inline=True,
                                            ),    
                                        ),
                                        id="collapse-priority",
                                    ),
                                ]
                            ),
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        dbc.Row([
                                        html.B("Hospital"),
                                        daq.BooleanSwitch(
                                                        id="group-hospital-toggle",
                                                        color=color_s,
                                                        on=False,
                                                        style={"border-color":color_s, "align-content":"right"},
                                                        ),
                                        ])
                                    ),
                                    dbc.Collapse(
                                        dbc.CardBody(
                                            dcc.Dropdown(
                                                id='hospital_dropdown',
                                                options=[
                                                    {'label': element, 'value': element}
                                                    for element in df["hospital_name"].unique()
                                                ],
                                                value=None,
                                                multi=True
                                            ),
                                        ),
                                        id="collapse-hospital",
                                    ),
                                ]
                            ),
                            dbc.Button("APPLY FILTERS", 
                                   block=True,
                                   style={"backgroundColor":color_s,"border-color":color_s,"margin-top":"5px"}),
                            dbc.Button("CLEAR FILTERS",  
                                   block=True,
                                   style={"backgroundColor":"#E4E6EA","border-color":"red","color":"red"}),
                            ],
                        ),
                    ),
                    ],
                    id="poptest",
                    target="filter-button",
                    is_open=False,
                    placement="bottom",
                    style={"backgroundColor":"#00000029","width":"400px"}
                ),
                ],
                width=2,
            ),
            dbc.Col(
                [
                dbc.Button(
                    html.Center(
                    [
                    html.Img(src='assets/dcsv.svg', style={'height':'30%', 'width':'30%', "position":"relative","margin":"auto"}),
                    html.Div(html.B("DOWNLOAD CSV"), style={"color":color_s}),
                    ],
                    ),
                    id="download-button",
                    color=None
                ),
                Download(id="download"),
            
                dbc.Modal(
                    [
                    dbc.ModalHeader("DOWNLOAD"),
                    dbc.ModalBody("Downloads aren't avaliable yet!"),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close", className="ml-auto", style={"backgroundColor":color_s,"border":"none"})
                    ),
                    ],
                    id="modal",
                ),
                
                ],
                width=2,
                style={"color":color_s,}
            ),
            ],
            align="start",
            style={
                "backgroundColor":"#E9F7F7",
                "padding-top":"20px"},
        ),
        dbc.Row(
            [
            dbc.Col(
                [
                dcc.Graph(
                id='dd-output-container',
                ),   
                ]
                ),
            dbc.Col(
                [
                html.Div(id="table")
                ]
            ),
            ],
            style={"display": "flex","justify-content": "space-between","margin":"30px"}
        )
    ]
)
    
], style={"backgroundColor":"#F6F7F9",
          "padding-top":"5px",
          "padding-bottom":"5px",})

@app.callback(
    Output("modal", "is_open"),
    [Input("download-button", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("poptest", "is_open"),
    [Input("filter-button", "n_clicks"),
     Input("filter-clear", "n_clicks")],
    [State("poptest", "is_open")],
)
def toggle_popover_2(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("collapse-coordinates", "is_open"),
    [Input("group-coordinates-toggle", "on")],
    [State("group-coordinates-toggle", "is_open")],
)
def toggle_coordinates(on, is_open):
    if on:
        return not is_open
    return is_open

@app.callback(
    Output("collapse-type", "is_open"),
    [Input("group-type-toggle", "on")],
    [State("group-type-toggle", "is_open")],
)
def toggle_type(on, is_open):
    if on:
        return not is_open
    return is_open

@app.callback(
    Output("collapse-gender", "is_open"),
    [Input("group-gender-toggle", "on")],
    [State("group-gender-toggle", "is_open")],
)
def toggle_gender(on, is_open):
    if on:
        return not is_open
    return is_open

@app.callback(
    Output("collapse-priority", "is_open"),
    [Input("checklist-priority-toggle", "on")],
    [State("checklist-priority-toggle", "is_open")],
)
def toggle_priority(on, is_open):
    if on:
        return not is_open
    return is_open

@app.callback(
    Output("collapse-hospital", "is_open"),
    [Input("group-hospital-toggle", "on")],
    [State("group-hospital-toggle", "is_open")],
)
def toggle_hospital(on, is_open):
    if on:
        return not is_open
    return is_open

@app.callback(
    Output('dd-output-container', 'figure'),
    Output('table', 'children'),
    [Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input("collapse-priority", "is_open"),
    Input("radioitems-inline-input",'value'),
    Input("collapse-gender", "is_open"),
    Input("group-gender-items", "value"),
    Input("collapse-hospital", "is_open"),
    Input("hospital_dropdown", "value")])

def run_query(start_date,end_date,is_priority,priority_list,is_gender,gender,is_hospital,hospital_list):
    
    df2 = pd.read_sql("""
    select * 
    from ic.calls
    WHERE beginning BETWEEN '{}'::timestamp
                 AND '{}'::timestamp  
    """.format(start_date,end_date), conn)
    
    if is_priority:
        df2 = df2[df2["priority"].isin(priority_list)]
    if is_gender:
        df2 = df2[df2["gender"] == gender]
    if is_hospital:
        df2 = df2[df2["hospital_name"].isin(hospital_list)]
    
    fig = px.density_mapbox(df2, lat = 'lat', lon = 'lng', 
                        center = dict(lat = -22.485872118888633, lon = -43.47397803653647), zoom = 8,
                        #color_continuous_scale = "blues",
                        mapbox_style = "open-street-map",
                        hover_data = {"victim_age":True, 
                                      "hospital_name":True, 
                                      "gender":True})
    fig.update_layout(margin = {"r":0,"t":0,"l":0,"b":0})
    
    table = dash_table.DataTable(
                    id='datatable-interactivity',
                    columns=[
                        {"name": i, "id": i, "deletable": True, "selectable": True} for i in df2.columns
                    ],
                    data=df2.to_dict('records'),
                    export_format="csv",
                    export_headers='display',
                    editable=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable="single",
                    row_selectable="multi",
                    row_deletable=True,
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    page_size= 30,
                    fixed_rows={'headers': True},
                    style_header={'backgroundColor': 'white','fontWeight': 'bold'},
                    style_as_list_view=True,
                    style_data={
                        'heigth': '100%', 'minWidth': '15px', 'maxWidth': '50px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'transparent'
                        }
                    ],
                ),
    
    return fig, table


if __name__ == '__main__':
    app.run_server(debug=False, port=2024)