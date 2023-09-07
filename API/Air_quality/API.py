import requests
import pandas as pd

response = requests.get('https://api.gios.gov.pl/pjp-api/rest/station/findAll')
monitoring_stations = response.json()

df = pd.DataFrame(monitoring_stations)
df = df.drop(columns=['city', 'addressStreet'])
station_ids = df['id'].tolist()

sensors_list = []

for station_id in station_ids:
    response = requests.get(f"https://api.gios.gov.pl/pjp-api/rest/station/sensors/{station_id}")

    if response.status_code == 200:
        sensors = response.json()
        sensors_list.append(sensors)
    else:
        print(f"Błąd przy pobieraniu danych dla stacji o ID {station_id}")

flattened_data = [item for sublist in sensors_list for item in sublist]
df_2 = pd.DataFrame(flattened_data)
param_df = pd.json_normalize(df_2['param'])
df_2 = df_2.drop(columns=['param'])
df_2 = pd.concat([df_2, param_df], axis=1)

merged_df = pd.merge(df, df_2, left_on='id', right_on='stationId')
merged_df = merged_df.rename(columns={'id_y': 'sensor_id'})
merged_df = merged_df.drop(columns=['id_x'])

columns_renamed = {
    'stationName': 'station_name',
    'gegrLat': 'latitude',
    'gegrLon': 'longitude',
    'sensor_id': 'sensor_id',
    'stationId': 'station_id',
    'paramName': 'pollutant',
    'paramFormula': 'pollutant_symbol',
    'paramCode': 'pollutant_code',
    'idParam': 'pollutant_id'
}
merged_df = merged_df.rename(columns=columns_renamed)

merged_df.to_csv('monitoring_stations_PL.csv', index=False)
