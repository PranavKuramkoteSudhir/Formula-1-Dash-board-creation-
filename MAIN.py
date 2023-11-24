from dash_visualization import create_f1_dashboard_app
from data_extraction import PySparkMySQLExtractor

connection_properties = {"url": "jdbc:mysql://127.0.0.1:3306/formula2", "user": "root", "password": "", "driver": "com.mysql.cj.jdbc.Driver"}
extractor = PySparkMySQLExtractor(connection_properties)
pandas_result = extractor.extract_table_to_pandas("results")
pandas_races = extractor.extract_table_to_pandas("races")
pandas_circuits = extractor.extract_table_to_pandas("circuits")
pandas_drivers = extractor.extract_table_to_pandas("drivers")
pandas_pit_stops = extractor.extract_table_to_pandas("pit_stops")
pandas_constructors = extractor.extract_table_to_pandas("constructors")
extractor.close_spark_session()
merged_df = pandas_result.merge(pandas_races[['raceId', 'circuitId', 'year']], on='raceId')
merged_df = merged_df.drop('raceId', axis=1)
merged_df = merged_df.merge(pandas_circuits[['circuitId', 'circuitRef']], on='circuitId')
merged_df = merged_df.drop('circuitId', axis=1)
merged_df = merged_df.merge(pandas_drivers[['driverId', 'forename', 'surname']], on='driverId')
pit_df=  pandas_pit_stops.merge(pandas_result[['raceId', 'driverId', 'constructorId']], on=['raceId', 'driverId'], how='left')
pit_df= pit_df.merge(pandas_constructors[["constructorId","name"]], on="constructorId")
merged_df['position_difference'] = merged_df['position'] - merged_df['grid']

merged_df['circuit_year'] = merged_df['circuitRef'] + '_' + merged_df['year'].astype(str)
pit_df = pit_df.merge(pandas_races[['raceId', 'circuitId', 'year']], on='raceId')
average_milliseconds_per_year_per_name = pit_df.groupby(['year', 'name'])['milliseconds'].mean().reset_index()
print(merged_df.columns)
result_df = merged_df.groupby(['year', 'driverId', 'forename', 'surname']).agg(points=('points', 'sum')).reset_index()
result_df['forename'] = result_df['forename'] + ' ' + result_df['surname']



f1_app = create_f1_dashboard_app(merged_df, average_milliseconds_per_year_per_name, result_df )

# Run the app
f1_app.run_server(debug=True)

