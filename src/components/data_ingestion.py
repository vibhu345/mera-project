import os #Operating System से जुड़े कार्यों के लिए (जैसे फ़ाइलें मैनेज करना, डायरेक्टरी बनाना, आदि)।
import sys # sys → System-specific पैरामीटर और फंक्शन को एक्सेस करने के लिए।
import numpy as np
import pandas as pd
from  pymongo import MongoClient #MongoClient को import किया गया है ताकि हम MongoDB database से connect कर सकें।
from zipfile import Path# यह फ़ाइलों की path handling के लिए उपयोग होता है।
from src.constant import *
from src.exception import CustomException
from src.logger import logging
from src.utils.main_utils import MainUtils
from dataclasses import dataclass 
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler,FunctionTransformer,StandardScaler
from sklearn.pipeline import Pipeline
#  हमें constructor (__init__ method), __repr__ method, और __eq__ method नहीं लिखना पड़ता।
# for eg without data class
# class Student:
#     def __init__(self, name, age, grade):
#         self.name = name
#         self.age = age
#         self.grade = grade

#     def __repr__(self):
#         return f"Student(name={self.name}, age={self.age}, grade={self.grade})"

# # Object Createion
# student1 = Student("Vibhanshu", 22, "A")
# with dataclass
# from dataclasses import dataclass
# @dataclass
# class Student:
#     name: str
#     age: int
#     grade: str
# # Object Createion
# student1 = Student("Vibhanshu", 22, "A")

@dataclass
class DataIngestionConfig:
    artifact_folder:str=os.path.join(artifact_folder)# current directry se artifact_folder ka path le aaye
class DataIngestion:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()
        self.utils=MainUtils()
    def export_mongo_collection_to_csv(self, collection_name, db_name) -> str:
        try:
            logging.info("Mongo danav se data cheene ki taiyaari hai")
            mongo_client=MongoClient(MONGO_DB_URL) # mongo db se connect kar rahe hai
            collection=mongo_client[db_name][collection_name] # mongo db se data fetch kar rahe hai
            df=pd.DataFrame(list(collection.find()))#fetch kiye hue data ko dataframe mein convert kar rahe hai
            logging.info("Sarkar mongo danav har gya,hum jjjjjjjjeeeeeeeeeeeeeeet gaye")
            df=df.replace("na",np.nan) 
            raw_file_path=self.data_ingestion_config.artifact_folder # dataframe mein toh convert kar liya lekin iss data ko jaha store karna hai waha jaane ka rassta malum hona chahiye
            os.makedirs(raw_file_path,exist_ok=True) # raste se hote hue ghar tak pahuch gye
            feature_store_file_path=os.path.join(raw_file_path,"wafer.csv")
            #raw_file_path → Directory (Folder) का path देता है।
            #feature_store_file_path → उस directory के अंदर file का पूरा path देता है
            df.to_csv(feature_store_file_path,index=False)
            logging.info("Data ko csv mein convert kar diya,rajya hamara hua")
            return feature_store_file_path
        except Exception as e:
            raise CustomException(e,sys)
    def initiate_data_ingestion(self)-> Path:
        logging.info("Bhai data ingestion wala module shuru hone jaaraha hai")
        try:
            feature_store_file_path=self.export_mongo_collection_to_csv(MONGO_COLLECTION_NAME,MONGO_DATABASE_NAME)
            logging.info("got the data from mongodb")
            logging.info("exited initiate_data_ingestion methods of data ingestion class")
            return feature_store_file_path
        except Exception as e:
            raise CustomException(e,sys) from e
        # from e ka simple matlab kya hai?
# Agar ek error ki wajah se dusra error aata hai, to from e use karne se original error bhi dikhai deta hai.
# Agar from e na likhein, to sirf naya error dikhega, purana error chhup jayega.


            



        
    

        


