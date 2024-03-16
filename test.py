from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
from supabase import create_client, Client

# url: str = 'https://zdrgurrkwghrbtzfttmf.supabase.co'
# key: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpkcmd1cnJrd2docmJ0emZ0dG1mIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDc1NzI1NzYsImV4cCI6MjAyMzE0ODU3Nn0.g8HNHTMNXp_2qiTqbe4_GtzyYZuNd-96X8MqMK5QUSM'
# supabase: Client = create_client(url, key)

# data, count=supabase.table('dataset').select("input_sequence").eq('id_lahan', 1).order('input_sequence', desc=True).limit(1).execute()
# sequence = data[1][0]['input_sequence']
# data,count = supabase.table('dataset').select("moisture_before").eq('input_sequence', sequence).execute()
# moist_before = data[1][0]['moisture_before']
# data, count = supabase.table('dataset').insert({"id_lahan": 1, "moisture_before": moist_before,"weather_code": 1,"moisture_after": 2500}).execute()
	

dataset = pd.read_csv('moisture_before_after_1.csv')
dataset = dataset[dataset['moisture_after'] != -1]
print(dataset)
