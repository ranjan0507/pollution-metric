import pandas as pd

def build_dataset(aqi_df,weather_df,trends_df):
	aqi_df['date'] = aqi_df['date.utc'].dt.date

	daily_sensor = aqi_df.groupby(['date','location'])['pm25'].mean().reset_index()