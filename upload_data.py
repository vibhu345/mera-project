# when we run this file code it will read the dataset and upload the dataset to mongo db
from pymongo.mongo_client import MongoClient
import pandas as pd
import json #json: JSON डेटा को handle करने के लिए यह library useful होती है।
url="mongodb+srv://vibhanshugupta875:VfyONMmrG1fWKn6V@cluster0.zsxdo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# create a new client and connect to server
client=MongoClient(url)
# create a database name and collection name
database_name="vibhanshu875" # kuch bhi naam de sakte ho
collection_name='data' # kuch bhi naam de sakte ho
df=pd.read_csv("C:\Users\vibha\Downloads\mera pehla project\notebooks\wafer.csv")
df.head()
if "Unnamed: 0" in df.columns:
    df=df.drop("Unnamed: 0",axis=1)
df
# data ko json mein convert karenge taaki hum iss data ko mongo db pe upload kar sake
json_record=list(json.loads(df.T.to_json()).values())
json_record
client[database_name][collection_name].insert_many(json_record)