import sys
import os
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
 
external_stylesheets = ["https://fonts.googleapis.com/icon?family=Material+Icons","https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)#,requests_pathname_prefix='/Waec_Statistics/')
app.scripts.config.serve_locally = True

read_waec_data = pd.read_csv(os.path.join(basedir,'assets','Waec_2016_2018.csv')) # Loading the merged prices
#---------------------------------------------------------------
#Defining The variables
waec_data = read_waec_data.copy() # The full sheet, copied to preserve the original version
years = waec_data.YEAR.unique() # Available WAEC exam data years
school_type = waec_data.SCHOOL_TYPE.unique() #Either PRIVATE or PUBLIC
metrics = waec_data.METRICS.unique() # Criteria to access
gender = waec_data.GENDER.unique() # Either MALE or FEMALE
locations = waec_data.columns[4:] # the list of all states with the addition ABUJA, NIGERIA & OFFSHORE

#----------------------------------------------------------------
'''
states_food_prices=states_food_data.copy()
item_list = states_food_prices.ItemLabels.unique()
data_months = list(states_food_prices.columns)[2:]
state_list = states_food_prices.States.unique()
'''
#----------------------------------------------------------------
#setting the template variables
with open(os.path.join(basedir,'assets','side_bar.html')) as f:
    sidebar_content = f.read()
    
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
    className="row",
    children=[
        
        #------------- The left side of the screen -----------#
        html.Div(
            className="col-xs-12 col-sm-6",
            children= [
                dcc.Dropdown(
                    #id='left_metrics',
                    options=[{'label': i, 'value': i} for i in metrics],
                    value="5 CREDITS & ABOVE INCLUDING MATHEMATICS & ENGLISH LANG."
                ),
                html.Div(
                    className="col-xs-8",
                    style={"padding":"0","padding-top":"15px"},
                    children= [
                        dcc.Dropdown(
                            #id='left_location',
                            options=[{'label': i, 'value': i} for i in locations],
                            value=['NIGERIA']
                        ),
                        dcc.Dropdown(
                            #id='left_type',
                            options=[{'label': i, 'value': i} for i in school_type],
                            value=['PRIVATE']
                        ),
                    ],
                ),
                html.Img(
                    className="col-xs-4",
                    style={"width":"100px","padding":"10px", "border-radius": "50%","float":"right"},
                    src=app.get_asset_url("Private Result.jpg")
                ),
                #for year in years:
                dash_table.DataTable(
                    #id='left_table',
                    columns=[
                        {"name":"Metric","id": "metric"},
                        {"name":"Male","id": "Male"},
                        {"name":"Female","id": "Female"},
                        {"name":"Total","id": "Total"},
                    ],
                    style_header={
                        'backgroundColor':'rgb(230,230,230)',
                        'fontWeight':'bold',
                        'textAlign':'center',
                    }
                ),
            ],    
        ),
        
        

        #-------- The right side of the screen-----------#
        html.Div(
            className="col-xs-12 col-sm-6",
            children= [
                dcc.Dropdown(
                    #id='right_metrics',
                    options=[{'label': i, 'value': i} for i in metrics],
                    value="5 CREDITS & ABOVE INCLUDING MATHEMATICS & ENGLISH LANG."
                ),
                
                html.Img(
                    className="col-xs-4",
                    style={"width":"100px","padding":"10px", "border-radius": "50%"},
                    src=app.get_asset_url("Public Result2.jpg")
                ),
                html.Div(
                    className="col-xs-8",
                    style={"padding":"0","margin":"0px", "padding-top":"15px","float":"right"},
                    children= [
                        dcc.Dropdown(
                            #id='right_location',
                            options=[{'label': i, 'value': i} for i in locations],
                            value=['NIGERIA']
                        ),
                        dcc.Dropdown(
                            #id='right_type',
                            options=[{'label': i, 'value': i} for i in school_type],
                            value=['PUBLIC']
                        ),
                    ],
                ),
            ],
        ),        
        
        
        
        
        
    ],
)
        
if __name__ == '__main__':
    app.run_server(debug=True)
    