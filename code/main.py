# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 16:16:21 2019

@author: srahman
"""
import plotly.express as px
import plotly.figure_factory as ff
import dash
import dash_table as dt
from dash_table.Format import Format
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import ibd_history as ibd
import tnf_ibd as tnf
import pandas as pd
import plotly.graph_objects as go
import copy

fig=go.Figure()
app = dash.Dash()
app.config['suppress_callback_exceptions']=True
app.title='Reprocell IBD Drug Discovery'
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})

range_columns=[{'label':'SEB5ASA_SEB', 'value':'SEB5ASA_SEB_Range'},
                {'label':'SEBPred1uM_SEBDMSO', 'value':'SEBPred1uM_SEBDMSO_Range'},
                {'label':'SEBPred100nM_SEBDMSO', 'value':'SEBPred100nM_SEBDMSO_Range'},
                {'label':'SEBBirb796100nM_SEBDMSO', 'value':'SEBBirb796100nM_SEBDMSO_Range'},
                {'label':'SEBBirb79610nM_SEBDMSO', 'value':'SEBBirb79610nM_SEBDMSO_Range'}]






layout = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc'    
   )
layout_right = copy.deepcopy(layout)
layout_right['height'] = 300
layout_right['margin-top'] = '20'
layout_right['font-size'] = '12'


tab1_layout = html.Div(
    [
      
        html.H3("Compound Effect on TNF Release"),
        html.Div(
            [
                html.P([d + ":", dcc.Dropdown(id=d, options=tnf.col_options)])
                for d in tnf.dimensions
                
            ],
            style={"width": "25%", "float": "left"},
            
        ),
        dcc.Graph(id="tnfgraph", style={"width": "75%", "display": "inline-block"}),
    ]
)

tab2_layout = html.Div(
    [
      
        html.H3("Comparative Analysis of Various Compounds"),
        html.Div(
            [
                
                   html.P(['Variables' + ":", dcc.Dropdown(id='my_drop', options=[{'label':m, 'value':m}
                                                           for m in tnf.tnf_compare.columns[2:6]], multi=True)])
                
                
            ],
            style={"width": "25%", "float": "left"},
        ),
        dcc.Graph(id="tnfgraphmulti", style={"width": "75%", "display": "inline-block"}),
    ]
)
        
tab3_layout = html.Div(
    [
      #tnf.tnf_mean_compare_i_r
        html.H3("TNF Reduction & Increase"),
        html.Div(
            [
                dt.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in sorted(tnf.tnf_ir.columns)],
                        #data=tnf.tnf_ir.to_dict('records'),
                        fixed_columns={ 'headers': True, 'data': 1 },
                        sort_action='custom',
                        sort_by=[],
        sort_mode="single",
    
    style_data_conditional=[
        {
            'if': {
                'column_id': 'SEB5ASA_SEB',
                'filter_query': '{SEB5ASA_SEB} < 0'
            },
            'backgroundColor': 'red',
            'color': 'white',
        },
        {
            'if': {
                'column_id': 'SEBPred1uM_SEBDMSO',
                'filter_query': '{SEBPred1uM_SEBDMSO} < 0'
            },
            'backgroundColor': 'red',
            'color': 'white',
        },
                    
         {
            'if': {
                'column_id': 'SEBPred100nM_SEBDMSO',
                'filter_query': '{SEBPred100nM_SEBDMSO} < 0'
            },
            'backgroundColor': 'red',
            'color': 'white',
        },             
        
        {
            'if': {
                'column_id': 'SEBBirb796100nM_SEBDMSO',
                'filter_query': '{SEBBirb796100nM_SEBDMSO} < 0'
            },
            'backgroundColor': 'red',
            'color': 'white',
        },
        {
            'if': {
                'column_id': 'SEBBirb79610nM_SEBDMSO',
                'filter_query': '{SEBBirb79610nM_SEBDMSO} < 0'
            },
            'backgroundColor': 'red',
            'color': 'white',
        }            
        ],
    style_cell={
        # all three widths are needed
        'minWidth': '40px', 'width': '180px', 'maxWidth': '180px',
        'whiteSpace': 'no-wrap',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
    },
            style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    },
            style_table={
        'maxHeight': '300px',
        'maxWidth': '800px',
        'overflowX': 'scroll',
        'overflowY': 'scroll',
        'border': 'thin lightgrey solid'
    },
    css=[{
        'selector': '.dash-cell div.dash-cell-value',
        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
    }]
                                    )#dt.DataTable
            ], className="six columns")
    ]
) #tab3_layout


tab4_layout = html.Div(
    [
      
        html.H3("TNF and Clinical Data (Scatter Plot)"),
        html.Div(
            [
                html.P([d + ":", dcc.Dropdown(id=d, options=tnf.tnf_ibd_col_options)])
                for d in tnf.dimensions
            ],
            style={"width": "25%", "float": "left"},
        ),
        dcc.Graph(id="tnfibdgraph", style={"width": "75%", "display": "inline-block"}),
    ]
) #tab3_layout

tab5_layout = html.Div(
    [
      
        html.H3("TNF and Clinical Data (Bar Plot)"),
        html.Div(
            [
                html.P([d + ":", dcc.Dropdown(id=d, options=tnf.tnf_ibd_col_options)])
                for d in ibd.dimensions
            ],
            style={"width": "25%", "float": "left"},
        ),
        dcc.Graph(id="tnfibdgraph_bar", style={"width": "75%", "display": "inline-block"}),
    ]
) #tab4_layout
        
tab6_layout = html.Div(
    [
      
        html.H3("Multiple Clinical Variables"),
        html.Div(
            [
                html.P([d + ":", dcc.Dropdown(id=d, options=ibd.col_options)])
                for d in ibd.dimensions
            ],
            style={"width": "25%", "float": "left"},
        ),
        dcc.Graph(id="ibdgraph", style={"width": "75%", "display": "inline-block"}),
    ]
)

tab7_layout = html.Div(
    [
      #tnf.tnf_mean_compare_i_r
        html.H3("Responders Groups"),
         
#        html.Div([ dcc.Slider(
#        id='my-slider',
#        min=5,
#        max=50,
#        #step=5,
#        marks={
#        5: '5',
#        10: '10',
#        15: '15',
#        20: '20',
#        25: '25',
#        50:'50'        
#    },
#        value=25,
#    ),
#    html.Div(id='slider-output')
#],className="row" ,
#        style = {'width' : '40%', 'height': '50px',
#                                    'fontSize' : '20px',
#                                    'padding-left' : '50px',
#                                    'display': 'inline-block'}
#    ), 
        
        html.Div(
            [
                dt.DataTable(
                        id='rtable',
                        columns=[{"name": i, "id": i, 'format':Format(precision=2)} for i in sorted(tnf.range_dfs.columns)],
                        #data=tnf.range_dfs.to_dict('records'),
                        sort_action='custom',
                        sort_by=[],
        sort_mode="single",
                        fixed_columns={ 'headers': True, 'data': 1 },
    style_cell={
        # all three widths are needed
        'minWidth': '40px', 'width': '180px', 'maxWidth': '180px',
        'whiteSpace': 'no-wrap',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
    },
            style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    },
            style_table={
        'maxHeight': '500px',
        'maxWidth': '800px',
        'overflowX': 'scroll',
        'overflowY': 'scroll',
        'border': 'thin lightgrey solid'
    },
    css=[{
        'selector': '.dash-cell div.dash-cell-value',
        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
    }]
                                    )
            ], className="six columns"),
                
   
    
    html.Div(
            [
                
                   html.P(['Variable' + ":", dcc.Dropdown(id='range_drop', options=range_columns)
                
                
            ],
            style={"width": "25%", "float": "left"}
        )    
    
   

    ],
            style=layout_right,
            className="two columns"),
            
#   html.Div(
#            [
#                
#                   html.P([dcc.RadioItems(id='radio', 
#                        options=[{'label':r, 'value':r} for r in tnf.range_dfs['SEBBirb796100nM_SEBDMSO_Range'].unique()])
#                
#                
#            ],
#            style={"width": "25%", "float": "left"}
#        )    
#    
#   
#
#    ],
#            style=layout_right,
#            className="two columns"         
#)

], className="row")#tab7_layout

        
app.layout = html.Div([
    dcc.Tabs(id="tabs", value='1', children=[
        dcc.Tab(label='Compound Effect on TNF Release', value='1'),
        dcc.Tab(label='Comparative Analysis of Various Compounds', value='2'),
        dcc.Tab(label='TNF Reduction & Increase', value='3'),
        dcc.Tab(label='TNF and Clinical Data (Scatter Plot)', value='4'),
        dcc.Tab(label='TNF and Clinical Data (Bar Plot)', value='5'),
        dcc.Tab(label='Multiple Clinical Variables', value='6'),
        dcc.Tab(label='Responders Groups', value='7')
    ]),
    html.Div(id='tab-output')
])






@app.callback(Output('tnfgraph', 'figure'), [Input(d, 'value') for d in tnf.dimensions])   
def make_figure(x, y, color):
     return px.scatter(
        #tnf.tnf_dfs_mean,  
        tnf.tnf_mean_compare_i_r,
        x=x,
        y=y,
        color='Donor_ID'
        
                  
    )

@app.callback(Output('tnfgraphmulti', 'figure'), [Input('my_drop', 'value')])   
def make_multifigure(values):
    traces=[]
    traces.append(go.Scatter(
            x=tnf.tnf_compare['SEB_mean'],
            y=tnf.tnf_compare['SEB5ASA_SEB'],
            text=tnf.tnf_compare['Donor_ID'],
            mode='markers',            
            name='SEB5ASA_SEB'
        ))
    for i in values:
            traces.append(go.Scatter(
            x=tnf.tnf_compare['SEBDMSO_mean'],
            y=tnf.tnf_compare[i],
            text=tnf.tnf_compare['Donor_ID'],
            mode='markers',            
            name=i
        ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': ''},
            yaxis={'title': 'TNF Release (% Control)'},            
            hovermode='closest'
        )
    }

@app.callback(
    Output('table', 'data'),
    [Input('table', 'sort_by')])
def update_table(sort_by):
    if len(sort_by):
        
        dff = tnf.tnf_ir.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dff = tnf.tnf_ir

    return dff.to_dict('records')

    
@app.callback(Output('tnfibdgraph', 'figure'), [Input(d, 'value') for d in tnf.dimensions])
def tnf_ibd_figure(x, y, color):
    return px.scatter(
        #tnf.tnf_dfs_mean,  
        tnf.tnf_ibd,
        x=x,
        y=y,
        color=color
    )

@app.callback(Output('tnfibdgraph_bar', 'figure'), [Input(d, 'value') for d in ibd.dimensions])
def tnf_ibd_bar(x, y, color,facet_col,facet_row):
    return px.bar(tnf.tnf_ibd, x=x, y=y, color=color, barmode="group", facet_col=facet_col,facet_row=facet_row)

#@app.callback(Output('intermediate-value', 'children'), [Input('my_dropdown', 'value')])
#def make_tnf_bar(selected_value):
    #r=tnf.get_drugs(selected_value)
    #uv=r[r.columns[0]].unique()
    
    #return px.bar(r, x=r.columns[2], color='Donor_ID', barmode="group")
    #table = []
    #if len(r) > 0:
        #table = r.to_dict('records')
    #return r.to_json()

#@app.callback(Output('drugcat', 'value'), [Input('intermediate-value', 'value')])
#def update_dtable(df):
    #cat = pd.read_json(df)
   # return cat['Donor_ID']

@app.callback(Output("ibdgraph", "figure"), [Input(d, 'value') for d in ibd.dimensions])
def make_ibdfigure(x, y, color, facet_col, facet_row):
    return px.bar(ibd.ibd_df, x=x, y=y, color=color, barmode="group", facet_col=facet_col,facet_row=facet_row,
       category_orders={"Sex": ["M", "F"]})


@app.callback(
    Output('rtable', 'data'),
    [Input('rtable', 'sort_by')])
def update_table_r(sort_by):
    if len(sort_by):
        dff = tnf.range_dfs.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dff = tnf.range_dfs

    return dff.to_dict('records')



@app.callback(
    Output('tab-output', 'children'),
    [Input('tabs', 'value')]
)
def show_content(value):
    if value == '1':
        return tab1_layout
    elif value == '2':
        return tab2_layout
    elif value == '3':
        return tab3_layout
    elif value == '4':
        return tab4_layout
    elif value == '5':
        return tab5_layout
    elif value == '6':
        return tab6_layout
    elif value == '7':
        return tab7_layout



if __name__ == "__main__":
    #app.run_server(debug=True, host='127.0.0.1', port=2019, use_reloader=False)
    app.run_server(debug=True, host='192.168.168.160', port=7001, use_reloader=False)