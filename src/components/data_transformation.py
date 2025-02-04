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
@dataclass
class DataTransformationConfig:
    artifact_folder1=os.path.join(artifact_folder)
    transformed_train_file_path=os.path.join(artifact_folder1,"tarin.npy")
    transformed_test_file_path=os.path.join(artifact_folder1,"test.npy")
    transformed_object_file_path=os.path.join(artifact_folder1,"preprocessor.pkl")
class DataTransformation:
    def __init__(self,feature_store_file_path):
        self.feature_store_file_path=feature_store_file_path
        self.data_transformation_config=DataTransformationConfig()
        self.utils=MainUtils()
    @staticmethod
    def get_data(feature_store_file_path:str)->pd.DataFrame:
        try:
            data=pd.read_csv(feature_store_file_path)
            data=data.rename(columns={'Good/Bad':TARGET_COLUMN})
            return data
        except Exception as e:
            raise CustomException(e,sys)
    def data_transform_kareahe_hai(self):
        try:
            preprocessor=Pipeline(steps=[("imputer",SimpleImputer()),("scalling",RobustScaler())])
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
    def initiate_data_transformation(self):
        logging.info("bhai data tranformation wala module shuru hone wala hai apni seta ki peti band lo")
        try:
            dataframe=self.get_data(self.feature_store_file_path)
            x=dataframe.drop(columns=TARGET_COLUMN)
            y=np.where(dataframe[TARGET_COLUMN]==-1,0,1)#targetcolumn mein jaha -1 hai usse 0 kar do aur 1 ko 1 hi rehne do
            x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=1)
            preprocessor=self.data_transform_kareahe_hai()
            x_train_scalled=preprocessor.fit_transform(x_train)
            x_test_scalled=preprocessor.transform(x_test)
            preprocessor_path=self.data_transformation_config.transformed_object_file_path
            os.makedirs(os.path.dirname(preprocessor_path,exist_ok=True))
        #    os.path.dirname(preprocessor_path) file path को directory path में बदल देता है।
        # os.makedirs() सिर्फ directory बनाएगा, file नहीं।
            self.utils.save_objects(file_path=preprocessor_path,obj=preprocessor)
            train_arr=np.c_(x_train_scalled,np.array(y_train))
            test_arr=np.c_(x_test_scalled,np.array(y_test))
            return (train_arr,test_arr,preprocessor_path)
        except Exception as e:
            raise CustomException (e,sys) from e






                                              

                                             