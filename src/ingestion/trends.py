from pytrends.request import TrendReq
import pandas as pd

def fetch_health_trends(start_date,end_date):
	pytrend = TrendReq(hl='en-US',tz=330)
	kw_list = ['cough','inhaler','pulmonologist']
	timeframe = f"{start_date} {end_date}"

	pytrend.build_payload(kw_list,cat=0,timeframe=timeframe,geo='IN-DL')
	df=pytrend.interest_over_time()
	
	if not df.empty and 'isPartial' in df.columns:
		df = df.drop(columns=['isPartial'])
	return df