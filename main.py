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
years = waec_data.YEAR.unique() # Available WAEC exam data years
school_type = list(waec_data.SCHOOL_TYPE.unique()) #Either PRIVATE, PUBLIC
school_type.append("ALL") # Add ALL to the selection,
metrics = waec_data.METRICS.unique() # Criteria to access
gender = waec_data.GENDER.unique() # Either MALE or FEMALE
locations = waec_data.columns[4:] # the list of all states with the addition ABUJA, NIGERIA & OFFSHORE

tabl_header = ["Metric","Male","Female","Total"]

#----------------------------------------------------------------
#setting the template variables
with open(os.path.join(basedir,'assets','side_bar.html')) as f:
    sidebar_content = f.read()
    
external_stylesheets = ["https://fonts.googleapis.com/icon?family=Material+Icons","https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)#,requests_pathname_prefix='/Waec_Statistics/')
app.scripts.config.serve_locally = True
app.index_string = public_helpers.dashboard_template(page_title='Nigeria WAEC Results Statistics',
                         page_subtitle='<strong class="green">Analyzing 2016 - 2018 Data</strong>',
                         meta_tag='Nigeria WAEC Results Data Analysis',
                         header_img_path='./assets/market9.jpg',
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
            style={"border": "5px solid white","backgroundColor":"grey", "borderRadius":"20px", "paddingBottom":"20px"},
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
                        ),],
                ),
                html.Img(
                    className="col-xs-6 col-sm-5",
                    style={"width":"130px","maxWidth":"100%","padding":"10px", "borderRadius": "50%","float":"right"},
                    src=app.get_asset_url("Private Result.jpg")
                ),
                
                html.Div( #Left Table
                    style={"clear":"both"},
                    children=[dcc.Store(id='memory-output'),
                    html.Div(
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
                    ),],
                ),],    
        ),
        
        #-------- The right side of the screen-----------#
        html.Div(
            className="col-xs-12 col-sm-6",
            style={"border": "5px solid white","backgroundColor":"grey", "borderRadius":"20px", "paddingBottom":"20px"},
                    
            children= [
                html.Img(
                    className="col-xs-6 col-sm-5",
                    style={"width":"130px","maxWidth":"100%","padding":"10px", "borderRadius": "50%"},
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
                        ),],
                ),
                
                html.Div( #Left Table
                    style={"clear":"both"},
                    children=[dcc.Store(id='r-memory-output'),
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
                    ),],
                ),],
        ),],
)
        
def data_need(location,year,select_type):
    '''Here, I generate the cell values'''
    year = int(year)
    #print(waec_data)
    state_waec = waec_data[["YEAR","SCHOOL_TYPE","METRICS","GENDER",location]] #Area of interest
    #getting the needed cells based on the selected year and school type
    if select_type != school_type[2]: #Use both public and private if ALL is selected
        #print(school_type, "of type ", type(school_type))
        print(select_type)
        state_waec = state_waec[state_waec.SCHOOL_TYPE==select_type]
    #state_data = state_waec[state_waec.YEAR==int(year)][location].to_list()
    state_data = state_waec[state_waec.YEAR==int(year)].groupby(["METRICS","GENDER"],sort=False,as_index=False).sum()[location].to_list()
    print(school_type)
    print("------")
    print(state_data)
    return(state_data)
    
def metric_compute(state_data):
    if isnan(state_data[0]):
        return [{tabl_header[0]:metrics[i],tabl_header[1]:'-', 
            tabl_header[2]:'-',tabl_header[3]:'-'} for i in range(len(metrics))]
    state_total_sat=state_data[0]+state_data[1]
    value =[state_data[0],state_data[1],state_total_sat] # initializing the cell value list
    for x in range(len(state_data)-2):
        i=x+2
        figure = int(state_data[i])
        if i%2!=1: # One total value for two consecutive elements
            total = f'{int(state_data[i]+state_data[i+1])} ({(state_data[i]+state_data[i+1])/state_total_sat * 100:.1f}%)'
            cell_value = f'{figure} ({figure/value[0] * 100:.1f}%)'
            value = value+[cell_value]
        else:
            cell_value = f'{figure} ({figure/value[1] * 100:.1f}%)'
            value = value+[cell_value]+[total]
    print(value)
    return [{tabl_header[0]:metrics[i],tabl_header[1]:value[i*3],
        tabl_header[2]:value[i*3+1],tabl_header[3]:value[i*3+2]} for i in range(len(metrics))]

#----Handling Left portion stuffs

@app.callback(dash.dependencies.Output('memory-output', 'data'),
              [dash.dependencies.Input('left_location', 'value'),
               dash.dependencies.Input('left_year','value'),
               dash.dependencies.Input('left_type', 'value')],
               [dash.dependencies.State('memory-output', 'data')]
)
def l_store_data(left_location,left_year,left_type, storage):
    data_of_interest = data_need(left_location,left_year,left_type)
    return data_of_interest


@app.callback(dash.dependencies.Output('left_table', 'data'),
              [dash.dependencies.Input('memory-output', 'data')])
def update_left_table(data):
    if data is None:
        raise dash.exceptions.PreventUpdate
    return metric_compute(data)

#----Handling Right portion stuffs

@app.callback(dash.dependencies.Output('r-memory-output', 'data'),
              [dash.dependencies.Input('right_location', 'value'),
               dash.dependencies.Input('right_year','value'),
               dash.dependencies.Input('right_type', 'value')],
               [dash.dependencies.State('r-memory-output', 'data')]
)
def r_store_data(right_location,right_year,right_type, storage):
    data_of_interest = data_need(right_location,right_year,right_type)
    return data_of_interest

@app.callback(dash.dependencies.Output('right_table', 'data'),
              [dash.dependencies.Input('r-memory-output', 'data')])
def update_right_table(data):
    if data is None:
        raise dash.exceptions.PreventUpdate
    return metric_compute(data)

        
if __name__ == '__main__':
    app.run_server(debug=True)