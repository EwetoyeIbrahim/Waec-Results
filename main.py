import sys
import os
from math import isnan
# Getting the base directory ensures that my resources are mobile
# especially in this development mode that I am yet to finalize the structure
basedir=os.path.abspath(os.path.dirname(__file__))
#sys.path.append(basedir) #When shred resources is within this folder
sys.path.append(os.path.join(basedir,os.path.pardir)) # when outside this folder
from _shared_res import public_helpers as public_helpers

import textwrap
#-----------------------------------------------------------
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objs as go
import plotly.tools as tls
#-----------------------------------------------------------
 

read_waec_data = pd.read_csv(os.path.join(basedir,'assets','Waec_2016_2018.csv')) # Loading the merged prices
#---------------------------------------------------------------
#Defining The variables
waec_data = read_waec_data.copy() # The full sheet, copied to preserve the original version
years = list(waec_data.YEAR.unique()) # Available WAEC exam data years
school_type = list(waec_data.SCHOOL_TYPE.unique()) #Either PRIVATE, PUBLIC
school_type.append("ALL") # Add ALL to the selection,
metrics = list(waec_data.METRICS.unique()) # Criteria to access
gender = list(waec_data.GENDER.unique()) # Either MALE or FEMALE
locations = waec_data.columns[4:] # the list of all states with the addition ABUJA, NIGERIA & OFFSHORE

tabl_header = ["Metric","Male","Female","Total"]

#----------------------------------------------------------------
#setting the template variables
colors={
        'graph_bg' : "white",
        'text' : "grey",
        'board_color': 'grey',
    }
with open(os.path.join(basedir,'assets','side_bar.html')) as f:
    sidebar_content = f.read()
    
external_stylesheets = ["https://fonts.googleapis.com/icon?family=Material+Icons","https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)#,requests_pathname_prefix='/Waec_Statistics/')
app.scripts.config.serve_locally = True
app.index_string = public_helpers.dashboard_template(page_title='Nigeria WAEC Results Statistics',
                         page_subtitle='<strong>Analyzing 2016 - 2018 Data</strong>',
                         meta_tag='Nigeria WAEC Results Data Analysis',
                         header_img_path='assets/Equimolar_white_s.png',
                         header_img_alt='Nigeria Food Prices',
                         links_to_related_files = '',
                         generated_advert='',
                         sidebar_content= sidebar_content,
                         list_of_recent_visuals='',
                         )
#-----------------------------------------------------------------

app.layout = html.Div(
    className="container-fluid row",
    children=[
        
        #------------- The left side of the screen -----------#
        html.Div(
            className="col-xs-12 col-sm-6",
            style={"border": "5px solid white","backgroundColor":"grey", 
                "borderRadius":"20px", "paddingBottom":"20px"},
            children= [
                html.Div(
                    className="col-xs-6 col-sm-7",
                    style={"padding":"0","paddingTop":"15px"},
                    children= [
                        dcc.Dropdown(
                            id='left_location',
                            options=[{'label': f'Location: {i}', 'value': i} for i in locations],
                            value='NIGERIA'
                        ),
                        dcc.Dropdown(
                            id='left_type',
                            options=[{'label': f'School Type: {i}', 'value': i} for i in school_type],
                            value='PRIVATE'
                        ),
                        dcc.Dropdown(
                            id='left_year',
                            options=[{'label': f'Year: {i}', 'value': i} for i in years],
                            value= 2018
                        ),
                    ],
                ),
                html.Img(
                    className="col-xs-6 col-sm-5",
                    style={"width":"130px","maxWidth":"100%",
                        "padding":"10px", "borderRadius": "50%","float":"right"},
                    src=app.get_asset_url("Private Result.jpg")
                ),
                #----------------------------------------------------------
                html.Div(
                    style={"clear":"both"},
                    children=[dcc.Graph(id='l-graph')],
                ),
                html.Div(
                    style={"clear":"both"},
                    className="table-responsive",
                    children= dash_table.DataTable(
                        id='left_table',
                        columns=[{"name":i,"id": i,"selectable": True} for i in tabl_header],
                        style_cell={
                            # all three widths are needed
                            'height': 'auto',
                            'minWidth': '100px', 'width':'100px','maxWidth': '180px',
                            'whiteSpace': 'normal'
                        },
                        sort_action="native",
                        page_action="native",
                    ),
                ),
                html.Div(#The summary section
                    className="col-xs-12", 
                    style={"padding-top":"20px"},
                    children= [
                        dcc.Markdown(id='l-summary-txt'),
                        ],
                ), 
            ],    
        ),
        
        

        #-------- The right side of the screen-----------#
        html.Div(
            className="col-xs-12 col-sm-6 hidden-xs",
            style={"border": "5px solid white","backgroundColor":colors['board_color'], "borderRadius":"20px",
                "paddingBottom":"20px"},
                    
            children= [
                html.Img(
                    className="col-xs-6 col-sm-5",
                    style={"width":"130px","maxWidth":"100%","padding":"10px", 
                        "borderRadius": "50%"},
                    src=app.get_asset_url("Public Result2.jpg")
                ),
                html.Div(
                    className="col-xs-6 col-sm-7",
                    style={"padding":"0","paddingTop":"15px","float":"right"},
                    children= [
                        dcc.Dropdown(
                            id='right_location',
                            options=[{'label': f'Location: {i}', 'value': i} for i in locations],
                            value='OGUN'
                        ),
                        dcc.Dropdown(
                            id='right_type',
                            options=[{'label': f'School Type: {i}', 'value': i} for i in school_type],
                            value='PUBLIC'
                        ),
                        dcc.Dropdown(
                            id='right_year',
                            options=[{'label': f'Year: {i}', 'value': i} for i in years],
                            value='2018'
                        ),
                    ],
                ),
                #-------------------------------------------------
                html.Div(
                    style={"clear":"both"},
                    children=[dcc.Graph(id='r-graph')],
                ),
                html.Div(
                    className="table-responsive",
                    children= dash_table.DataTable(
                        id='right_table',
                        columns=[{"name":i,"id": i,"selectable": True} for i in tabl_header],
                        style_cell={
                            # all three widths are needed
                            'height': 'auto',
                            'minWidth': '100px', 'width':'100px','maxWidth': '180px',
                            'whiteSpace': 'normal'
                        },
                        sort_action="native",
                        page_action="native",
                    ),
                ),
                html.Div(#The summary section
                    className="col-xs-12", 
                    style={"padding-top":"20px"},
                    children= [
                        dcc.Markdown(id='r-summary-txt'),
                        ],
                ), 
            ],
        ),  
    ],
)

        
def data_need(location,year,select_type):
    '''Here, I generate the cell values'''
    year = int(year)
    state_waec = waec_data[["YEAR","SCHOOL_TYPE","METRICS","GENDER",location]] #Area of interest
    #getting the needed cells based on the selected year and school type
    if select_type != school_type[2]: #Use both public and private if ALL is selected
        #print(select_type)
        state_waec = state_waec[state_waec.SCHOOL_TYPE==select_type]
    #state_data = state_waec[state_waec.YEAR==int(year)][location].to_list()
    else:
        state_waec = state_waec.groupby(["YEAR","METRICS","GENDER"],sort=False,as_index=False).sum()
    state_data = state_waec[state_waec.YEAR==int(year)][location].to_list()
    #print(state_waec)
    return  state_waec, state_data

def metric_compute(location,year,school_type):
    '''Here, I generate the cell values'''
    state_waec, state_data = data_need(location,year,school_type)
    #print(state_data)
    if isnan(state_data[0]):
        return [{tabl_header[0]:metrics[i],tabl_header[1]:'-', 
            tabl_header[2]:'-',tabl_header[3]:'-'} for i in range(len(metrics))]
    state_total_sat=state_data[0]+state_data[1]
    value =[state_data[0],state_data[1],state_total_sat] # initializing the cell value list
    for x in range(len(state_data)-2):
        i=x+2
        figure = int(state_data[i])
        if i%2!=1: # One total value for two consecutive elements
            total = f'''
                {int(state_data[i]+state_data[i+1])} 
                ({(state_data[i]+state_data[i+1])/state_total_sat * 100:.1f}%)
                '''
            cell_value = f'{figure} ({figure/value[0] * 100:.1f}%)'
            value = value+[cell_value]
        else:
            cell_value = f'{figure} ({figure/value[1] * 100:.1f}%)'
            value = value+[cell_value]+[total]
    output_data = [{tabl_header[0]:metrics[i],tabl_header[1]:value[i*3],
        tabl_header[2]:value[i*3+1],tabl_header[3]:value[i*3+2]} 
        for i in range(len(metrics))]
    summary_txt = summary_Txt(location.capitalize(),year,school_type.lower(),state_data,value)

    return output_data, summary_txt, state_waec

def summary_Txt(location,year,school_type,state_data,value):
    if school_type=='all':
        sat__with=' for the examination'
    else:
        sat__with='as '+ school_type + ' schools students'
    summary_txt = textwrap.dedent(f'''
        #### Summary: {location} | {year} | {school_type.capitalize()} Schools
        ----------------------
        The West African Examinations Council Results Statistics of **{year}** 
        for student's in {location} reflected that a total of **{value[2]}** 
        candidates sat {sat__with} with **{state_data[1]/(state_data[0]+state_data[1]) * 100:.1f}%** female and 
        **{state_data[0]/(state_data[0]+state_data[1]) * 100:.1f}%** male candidates.


        Of the {state_data[0]} male candidates, only **{state_data[-2]/state_data[0] * 100:.1f}%** 
        of them made 5 credits and above including Mathematics and English Language, 
        whereas out of the {state_data[1]}, **{state_data[-1]/state_data[1] * 100:.1f}%** 
        of them made 5 credits and above including Mathematics and English Language.  
        *Overall, The number of candidates with 5 credits and above 
        including Mathematics & English Language in {school_type} schools in 
        {location}({year})is put at **{value[-1]}**.*
        ''')

    return summary_txt

def update_graphs(location,state_waec,school_type):
    need_metric = ["TOTAL NUMBER SAT", "5 CREDITS & ABOVE INCLUDING MATHEMATICS & ENGLISH LANG."]
    state_waec2=state_waec[
        (state_waec.METRICS==need_metric[0]) | 
        (state_waec.METRICS==need_metric[1])
    ]

    #x=["TOTAL...", "5 CREDITS..."]
    #names = list(gender)
    num_val=state_waec2[state_waec2.columns[-1]].to_list()
    
    fig1 =[go.Bar(x=need_metric, y=[num_val[0],num_val[2]], name='',xaxis="x1",text=need_metric, legendgroup="Male"),
            go.Bar(x=need_metric, y=[num_val[1],num_val[3]], name='',xaxis="x1", text=need_metric, legendgroup="Female"),]

    #fig1.update_layout(barmode='stack',yaxis="y2")

    fig2 =[go.Bar(x=need_metric, y=[num_val[4],num_val[6]], name='',xaxis="x2",text=need_metric, legendgroup="Male",),
            go.Bar(x=need_metric, y=[num_val[5],num_val[7]], name='',xaxis="x2", text=need_metric, legendgroup="Female"),]

    fig3 =[go.Bar(x=need_metric, y=[num_val[8],num_val[10]], name='Male',xaxis="x3", text=need_metric, legendgroup="Male"),
            go.Bar(x=need_metric, y=[num_val[9],num_val[11]], name='Female',xaxis="x3", text=need_metric, legendgroup="Female"),]

    #fig2.update_layout(barmode='stack')
    data=fig1; data.extend(fig2); data.extend(fig3)
    
    layout = go.Layout(
        barmode='stack',
        xaxis= dict(
            tickvals=need_metric,
            ticktext=['Total..','5 Credits..'],
            domain= [0, 0.33],
            anchor= 'x1', 
            title= '2016'
        ),
        xaxis2= dict(
            tickvals=need_metric,
            ticktext=['Total..','5 Credits..'],
            domain= [0.33, 0.66],
            anchor= 'x2', 
            title= '2017'
        ),
        xaxis3= dict(
            tickvals=need_metric,
            ticktext=['Total....','5 Credits..'],
            domain= [0.66, 1],
            anchor= 'x3', 
            title= '2018'
        ),
    )
    
    fig ={'data':data, 'layout':layout}
    # Add image
    fig = go.Figure(fig)
    
    fig.update_layout(
        plot_bgcolor=colors['graph_bg'],
        font=dict(color=colors['text']),
        title=dict(
            text = f'''<i class="center-block"style="font-size: 12px; color:{colors['text']};">Graph of Total Candidates in {location} and Those That Had'''+
               "<br>5 or More Credits Including Maths and English</i>",
            y = 0.9, x=0.5,
            xanchor = 'center'),
        images = [dict(
            source="assets/Equimolar_s.png",
            xref="paper", yref="paper",
            x=1, y=0.95,
            sizex=0.30, sizey=0.30,
            xanchor="right", yanchor="bottom")]
    )
    
    #fig.show()
    
    return fig

def view_update(location,year,school_type):
    table_data, summary_txt, state_waec = metric_compute(location,year,school_type)
    fig = None
    fig = update_graphs(location.capitalize(),state_waec, school_type.capitalize())
    if table_data is None:
        raise dash.exceptions.PreventUpdate
    return table_data, fig, summary_txt


#----Handling Left portion stuffs

@app.callback(
    [dash.dependencies.Output('left_table', 'data'),
    dash.dependencies.Output('l-graph', 'figure'),
    dash.dependencies.Output('l-summary-txt', 'children'),],
    [dash.dependencies.Input('left_location', 'value'),
    dash.dependencies.Input('left_year','value'),
    dash.dependencies.Input('left_type', 'value')],)
def update_left(left_location,left_year,left_type):
    return view_update(left_location,left_year,left_type)
#----Handling Right portion stuffs

@app.callback(
    [dash.dependencies.Output('right_table', 'data'),
    dash.dependencies.Output('r-graph', 'figure'),
    dash.dependencies.Output('r-summary-txt', 'children'),],
    [dash.dependencies.Input('right_location', 'value'),
    dash.dependencies.Input('right_year','value'),
    dash.dependencies.Input('right_type', 'value')],)
def update_right(right_location,right_year,right_type):
    return view_update(right_location,right_year,right_type)

        
if __name__ == '__main__':
    app.run_server(debug=True)