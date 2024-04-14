# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                 dcc.Dropdown(id='site-dropdown',
                                              options=[
                                                {'label': 'All Sites', 'value': 'ALL'}] +
                                                [{'label': site, 'value': site} 
                                                 for site in spacex_df['Launch Site'].unique()],
                                                 value='ALL',
                                                placeholder="Select a Launch Site here",
                                                searchable=True,
                                                style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}),
                                                html.Br(),

                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)


                                

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks={0: '0', 10000: '10000'},
                                    value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_success_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Filter data to include all sites
        filtered_df = spacex_df
        title = 'Total Success Launches for All Sites'
    else:
        # Filter data for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        title = f'Total Success Launches for {selected_site}'

    # Create a pie chart
    fig = px.pie(filtered_df, names='class', title=title)
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), Input('payload-slider', 'value')]
)
def update_payload_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    if selected_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
        title = 'Payload vs. Success Scatter Plot for All Sites'
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == selected_site) & 
                                (spacex_df['Payload Mass (kg)'] >= low) & 
                                (spacex_df['Payload Mass (kg)'] <= high)]
        title = f'Payload vs. Success Scatter Plot for {selected_site}'
    
    fig = px.scatter(
        filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
        labels={"class": "Launch Success"}, title=title
    )
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
