from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
from supabase import create_client, Client

url: str = 'https://zdrgurrkwghrbtzfttmf.supabase.co'
key: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpkcmd1cnJrd2docmJ0emZ0dG1mIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDc1NzI1NzYsImV4cCI6MjAyMzE0ODU3Nn0.g8HNHTMNXp_2qiTqbe4_GtzyYZuNd-96X8MqMK5QUSM'
supabase: Client = create_client(url, key)

class Item(BaseModel):
	moisture: int
	moisture_limit:int
	id_lahan: int
	weather_code: int



app = FastAPI()

@app.post('/ml')
async def add_menu(item: Item):
	item_dict=item.dict()
	dataset_name=f'moisture_before_after_{item_dict.get("id_lahan")}.csv'
	with open(dataset_name, 'wb+') as f:
		res = supabase.storage.from_('ml-data-feeds').download(dataset_name)
		f.write(res)
	dataset = pd.read_csv(dataset_name)
	dataset = dataset[dataset['moisture_after'] != -1]
	X=dataset[['moisture_before', 'weather_code']]
	y=dataset['moisture_after'] 
	X=X.values
	y=y.values
	svr = DecisionTreeRegressor()
	svr.fit(X,y)	
	
	y_pred=svr.predict([[item_dict.get("moisture"),item_dict.get("weather_code")]])
	moisture_after=y_pred.tolist()
	if moisture_after[0] > item_dict.get("moisture_limit"):
		X=dataset[['moisture_after', 'weather_code']]
		y=dataset['moisture_before'] 
		X=X.values
		y=y.values
		svr = DecisionTreeRegressor()
		svr.fit(X,y)
		
		y_pred=svr.predict([[item_dict.get("moisture_limit"),item_dict.get("weather_code")]])
		moisture_after=y_pred.tolist()
	else:
		moisture_after[0]=-1
	data, count = supabase.table('dataset').select("input_sequence").eq('id_lahan', item_dict.get('id_lahan')).order('input_sequence', desc=True).limit(1).execute()
	sequence = data[1][0]['input_sequence']
	data, count = supabase.table('dataset').update({'moisture_after': item_dict.get('moisture')}).eq('input_sequence', sequence).execute()
	
	data, count = supabase.table('dataset').insert({"id_lahan": item_dict.get('id_lahan'), "moisture_before": item_dict.get('moisture'),"weather_code": item_dict.get('weather_code'),"moisture_after": -1}).execute()
	
	return moisture_after[0]
	

