import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

import pandas as pd



suicide = pd.DataFrame()
file_list = ['1999-2002.txt', '2003-2006.txt', '2007-2010.txt','2011-2014.txt','2015-2018.txt']
for file_name in file_list:
    tmp = pd.read_csv(file_name,sep='\t')
    tmp=tmp.drop(columns="Notes")
    tmp['Year'] = file_name
    tmp['Year'] = tmp['Year'].str.replace(r'.txt$', '')
    tmp['Year'] = tmp['Year'].str.split('-').str[1]
    tmp['Suicide_Death_Rate']=(tmp['Deaths']/tmp.Population)*100000
    tmp['County Code']=tmp['County Code'].astype(str)
    tmp['County Code']= tmp['County Code'].apply(lambda x: x.zfill(5))
    tmp=tmp.rename(columns={"County Code":"FIPS"})
    tmp['Year']=tmp['Year'].astype(int)

    tmp=tmp.drop(columns="Crude Rate")
    suicide = suicide.append(tmp)

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "1999-2002", "value": 2002},
                     {"label": "2003-2006", "value": 2006},
                     {"label": "2007-2010", "value": 2010},
                     {"label": "2011-2014", "value": 2014}],
                 multi=False,
                 value=2002,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})

])


import json
from urllib.request import urlopen
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = suicide.copy()
    dff = dff[dff["Year"] == option_slctd]

    # Plotly Express
    fig = px.choropleth_mapbox(dff, geojson=counties, color="Suicide_Death_Rate",
                           locations="FIPS",
                           hover_name="County", hover_data=["Deaths", "Population","Suicide_Death_Rate"],
                           center={"lat": 38.72490, "lon": -95.61446},
                           mapbox_style="carto-positron", zoom=3)

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#     fig.update_layout(
#         title_text="Bees Affected by Mites in the USA",
#         title_xanchor="center",
#         title_font=dict(size=24),
#         title_x=0.5,
#         geo=dict(scope='usa'),
#     )

    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False)
