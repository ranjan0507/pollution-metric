from meteostat import hourly
import pandas as pd

def fetch_weather(start_date,end_date):
	# wmo id for stations -> weather is assumed to be same in all delhi , so only 2 stations (safdarjung , palam)
	stations=['42182','42181']

	all_data=[]

	for station in stations:
		data = hourly(station,start_date,end_date)
		df = data.fetch()
		if not df.empty:
			df=df[['temp','rhum','wspd']]
			all_data.append(df)
	
	if all_data:
		new_df = pd.concat(all_data)
		delhi_mean_df = new_df.groupby(new_df.index).mean()
		return delhi_mean_df
	else:
		return pd.DataFrame()
