import pandas as pd

def build_dataset(aqi_df,weather_df,trends_df):
	aqi_df['date'] = aqi_df['date.utc'].dt.date

	daily_sensor = aqi_df.groupby(['date','location'])['pm25'].mean().reset_index()

	city_aqi = daily_sensor.groupby('date').agg(
		AQI_mean = ('pm25','mean'),
		AQI_max = ('pm25','max')
	)

	city_aqi.index = pd.to_datetime(city_aqi.index)

	weather = weather_df.resample('D').agg({
		'temp':'mean',
		'rhum':'mean',
		'wspd':'mean'
	})

	trends_df['health_index_raw'] = trends_df[['cough','inhaler','pulmonologist']].mean(axis=1)
	trends_df['health_index'] = trends_df['health_index_raw'].rolling(window=3).mean()

	df = city_aqi.join([weather,trends_df[['health_index']]],how='inner')
	df = df.interpolate(method='linear',limit=2).dropna()

	lag_features = ['AQI_mean','AQI_max','temp','wspd']

	for col in lag_features:
		for i in [1,2,3]:
			df[f'{col}_lag_{i}']=df[col].shift(i)
	
	return df.dropna()