import requests
import pandas as pd
import os

from dotenv import load_dotenv

import requests
import pandas as pd

def fetch_delhi_aqi(start_date, end_date):
    load_dotenv()
    api = os.getenv('aqi_key')
    
    headers = {"X-API-Key": api}
    
    loc_url = "https://api.openaq.org/v3/locations"
    
    loc_params = {
        "coordinates": "28.6139,77.2090",
        "radius": 25000,
        "limit": 100 
    }
    
    print("Fetching location IDs ")
    loc_response = requests.get(loc_url, params=loc_params, headers=headers)
    if loc_response.status_code != 200:
        raise Exception(f"Failed to fetch locations: {loc_response.text}")
        
    locations = loc_response.json().get('results', [])
    
    pm25_sensors = []
    location_mapping = {} 
    
    for loc in locations:
        for sensor in loc.get('sensors', []):
            if sensor.get('parameter', {}).get('name') == 'pm25':
                pm25_sensors.append(sensor['id'])
                location_mapping[sensor['id']] = loc['name']
    
    print(f"Found {len(pm25_sensors)} PM2.5 sensors")
    
    all_data = []
    for sensor_id in pm25_sensors:
        hours_url = f"https://api.openaq.org/v3/sensors/{sensor_id}/hours"
        hours_params = {
            "datetime_from": start_date,
            "datetime_to": end_date,
            "limit": 1000  
        }
        
        hours_response = requests.get(hours_url, params=hours_params, headers=headers)
        
        if hours_response.status_code == 200:
            results = hours_response.json().get('results', [])
            for row in results:
                dt = row.get('period', {}).get('datetimeFrom', {}).get('utc')
                
                if dt:
                    all_data.append({
                        'date.utc': dt,
                        'location': location_mapping[sensor_id],
                        'value': row['value']
                    })
        else:
            print(f"Warning: Failed to fetch data for sensor {sensor_id}")
                
    df = pd.DataFrame(all_data)
    if not df.empty:
        df['date.utc'] = pd.to_datetime(df['date.utc'])
        df.sort_values('date.utc', inplace=True)
        
    print(f" Successfully retrieved {len(df)} records.")
    return df

