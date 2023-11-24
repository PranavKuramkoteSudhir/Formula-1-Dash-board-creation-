import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

def create_f1_dashboard_app(merged_df, pit_stops_df, results_df):
    # Create a list of unique drivers with their names
    driver_options = [{'label': f"{row['forename']} {row['surname']}", 'value': f"{row['forename']} {row['surname']}"}
                      for _, row in merged_df[['forename', 'surname']].drop_duplicates().iterrows()]

    # Create a Dash web application
    app = dash.Dash(__name__)

    # Define the layout of the app
    app.layout = html.Div([
        html.H1("F1 Driver Positions Dashboard"),

        # First graph: Dropdown for selecting the driver
        dcc.Dropdown(
            id='driver-dropdown',
            options=driver_options,
            value=driver_options[0]['value'],  # Default selected driver (use the first driver name)
            multi=False,
        ),

        dcc.Graph(id='position-difference-graph'),

        # Second graph: Dropdown for selecting the year
        dcc.Dropdown(
            id='year-dropdown',
            options=[
                {'label': year, 'value': year}
                for year in merged_df['year'].unique()
            ],
            value=merged_df['year'].max(),  # Default to the latest year
            multi=False,
        ),

        # Second graph: Graph to display driver positions
        dcc.Graph(id='driver-positions-graph'),

        # Third graph: Average pit stops graph
        html.Div([
            dcc.Dropdown(
                id='pit-stop-year-dropdown',
                options=[
                    {'label': year, 'value': year}
                    for year in pit_stops_df['year'].unique()
                ],
                value=pit_stops_df['year'].max(),  # Default to the latest year
                multi=False,
                placeholder="Select Year for Average Pit Stops"
            ),
        ]),
        dcc.Graph(id='average-pit-stops-graph'),

        # Fourth graph: Results graph
        html.Div([
            dcc.Dropdown(
                id='results-year-dropdown',
                options=[
                    {'label': year, 'value': year}
                    for year in results_df['year'].unique()
                ],
                value=results_df['year'].max(),  # Default to the latest year
                multi=False,
                placeholder="Select Year for Total Points"
            ),
        ]),
        dcc.Graph(id='results-graph'),
    ])

    # Define callback to update the first graph based on the selected driver
    @app.callback(
        Output('position-difference-graph', 'figure'),
        [Input('driver-dropdown', 'value')]
    )
    def update_position_difference_graph(selected_driver_name):
        # Filter DataFrame for the selected driver
        selected_driver_df = merged_df[(merged_df['forename'] + ' ' + merged_df['surname']) == selected_driver_name]

        # Create a bar plot using Plotly Express
        fig = px.bar(
            selected_driver_df,
            x='circuit_year' if 'circuit_year' in merged_df.columns else 'circuitRef',
            y='position_difference' if 'position_difference' in merged_df.columns else 'position',
            title=f'Positions Gained/Lost ',
            labels={'position_difference': 'Position Difference', 'circuit_year': 'Circuit Year'}
        )

        # Customize the layout
        fig.update_layout(
            xaxis=dict(tickangle=45),
            yaxis=dict(
                title_text='Position Difference' if 'position_difference' in merged_df.columns else 'Position'),
            showlegend=True,
        )

        return fig

    # Define callback to update the second graph based on the selected year
    @app.callback(
        Output('driver-positions-graph', 'figure'),
        [Input('year-dropdown', 'value')]
    )
    def update_driver_positions_graph(selected_year):
        # Use .loc to avoid SettingWithCopyWarning
        selected_year_df = merged_df.loc[merged_df['year'] == selected_year].copy()

        # Create a scatter plot using Plotly Express
        fig = px.scatter(
            selected_year_df,
            x='circuit_year',
            y='position',
            color='forename',
            hover_name='forename',
            title=f'Driver Positions for Year {selected_year}',
            labels={'circuit_year': 'Circuit Year', 'position': 'Position'}
        )

        # Set a constant size for all data points
        fig.update_traces(marker=dict(size=8))

        # Customize the layout
        fig.update_layout(
            xaxis=dict(tickangle=45),
            yaxis=dict(autorange='reversed'),  # Reverse the Y-axis
            showlegend=True,
        )
        return fig

    # Define callback to update the third graph based on the selected driver
    @app.callback(
        Output('average-pit-stops-graph', 'figure'),
        [Input('pit-stop-year-dropdown', 'value')]
    )
    def update_average_pit_stops_graph(selected_year):
        # Filter pit_stops_df for the selected year
        selected_year_pit_stops_df = pit_stops_df[pit_stops_df['year'] == selected_year]

        # Calculate average pit stop time per name
        average_pit_stops_df = selected_year_pit_stops_df.groupby('name')['milliseconds'].mean().reset_index()

        # Create a bar plot using Plotly Express
        fig = px.bar(
            average_pit_stops_df,
            x='name',
            y='milliseconds',
            text='milliseconds',  # Display values on the bars
            title=f'Average Pit Stop Time for Year {selected_year}',
            labels={'milliseconds': 'Average Pit Stop Time (milliseconds)', 'name': 'Team'}
        )

        # Customize the layout
        fig.update_layout(
            xaxis=dict(tickangle=45),
            yaxis=dict(title_text='Average Pit Stop Time (milliseconds)'),
            showlegend=True,
        )

        return fig

    # Define callback to update the fourth graph based on the selected year
    @app.callback(
        Output('results-graph', 'figure'),
        [Input('results-year-dropdown', 'value')]
    )
    def update_results_graph(selected_year):
        # Filter results_df for the selected year
        selected_year_results_df = results_df[results_df['year'] == selected_year]

        # Calculate total points per driver
        total_points_df = selected_year_results_df.groupby(['forename', 'driverId'])['points'].sum().reset_index()

        # Create a bar plot using Plotly Express
        fig = px.bar(
            total_points_df,
            x='forename',
            y='points',
            color='driverId',  # Differentiate using driverId
            text='points',  # Display values on the bars
            title=f'Total Points for Year {selected_year}',
            labels={'points': 'Total Points', 'forename': 'Driver Forename', 'driverId': 'Driver ID'},
            hover_data=['driverId'],  # Display driverId in hover information
            color_discrete_map={'driverId': 'blue'}  # Set a single color for driverId
        )

        # Customize the layout
        fig.update_layout(
            xaxis=dict(tickangle=45),
            yaxis=dict(title_text='Total Points'),
            coloraxis_showscale=False,
            showlegend=False,  # Remove legend for driverId
        )

        return fig

    return app

if __name__ == '__main__':
    # Assuming merged_df is your DataFrame containing the race results
    # Assuming pit_stops_df is your DataFrame containing pit stop data
    # Assuming results_df is your DataFrame containing results data
    merged_df = ...
    pit_stops_df = ...
    results_df = ...

    # Create the F1 Dashboard app with pit stops and results
    f1_app = create_f1_dashboard_app(merged_df, pit_stops_df, results_df)

    # Run the app
    f1_app.run_server(debug=True)
