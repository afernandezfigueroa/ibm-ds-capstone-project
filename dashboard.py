# Import required libraries

import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_sites = spacex_df["Launch Site"].unique()

# Create a dash application

app = dash.Dash(name)

# Create an app layout

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                      # TASK 1: Add a dropdown list to enable Launch Site selection
                      # The default select value is for ALL sites
                      dcc.Dropdown(id='site-dropdown', 
                                   options=[{'label': 'All Sites', 'value': 'ALL'}] +
                                   [{'label': site, 'value': site} for site in launch_sites],
                                   value='ALL', searchable=True,
                                   placeholder="Select a Launch Site here"),
                      html.Br(),
                      # TASK 2: Add a pie chart to show the total successful launches count for all sites
                      # If a specific launch site was selected, show the Success vs. Failed counts for the site
                      html.Div(dcc.Graph(id='success-pie-chart')),
                      html.Br(),

                      html.P("Payload range (Kg):"),

                      # TASK 3: Add a slider to select payload range
                      dcc.RangeSlider(id='payload-slider',
                                      min=0,
                                      max=10000,
                                      step=1000,
                                      marks={0: '0', 1000: '1000',
                                             2000: '2000', 3000: '3000',
                                             4000: '4000', 5000: '5000',
                                             6000: '6000', 7000: '7000',
                                             8000: '8000', 9000: '9000',
                                             10000: '10000'},
                                             value=[min_payload, max_payload]),
                      # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                      html.Div(dcc.Graph(id='success-payload-scatter-chart')),])

# TASK 2:

# Add a callback function for site-dropdown as input, success-pie-chart as output

# Function decorator to specify function input and output

@app.callback(
Output(component_id='success-pie-chart', component_property='figure'),
Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):

if entered_site == 'ALL':
    # Select only successful launches
    successful_df = spacex_df[spacex_df['class'] == 1]

    # Count successful launches for each launch site
    site_success = successful_df.groupby('Launch Site').size().reset_index(name='Success Count')

    fig = px.pie(
        site_success,
        values='Success Count',
        names='Launch Site',
        title='Total Successful Launches By Site'
    )

    return fig

else:
    # Filter dataframe for the selected launch site
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]

    # Count successful and failed launches
    success_count = len(filtered_df[filtered_df['class'] == 1])
    failed_count = len(filtered_df[filtered_df['class'] == 0])

    fig = px.pie(
        values=[success_count, failed_count],
        names=['1', '0'],
        title=f'Total Succes Launches for {entered_site}'
    )

    return fig



# TASK 4:

# Add a callback function for site-dropdown and payload-slider as inputs, success-payload-scatter-chart as output

# Run the app

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def get_scatter_chart(entered_site, payload_range):

    # Filter dataframe based on payload range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]

    if entered_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Launch Success'
        )
    else:
        # Filter dataframe for the selected launch site
        filtered_df = filtered_df[
            filtered_df['Launch Site'] == entered_site
        ]

        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Correlation between Payload and Launch Success for {entered_site}'
        )

    return fig

if name == 'main':
app.run()