import shutil
# shutil Python ka ek built-in module hai jo file operations (copy, move, delete, compress, extract, etc.) ke liye use hota hai. Yeh os module se zyada powerful hai, kyunki yeh recursively directories aur symbolic links ke saath kaam kar sakta hai
import os
import sys
import pandas as pd
import pickle
from src.logger import logging
from src.exception import CustomException
from flask import request
from src.constant import *
from src.utils.main_utils import MainUtils
from dataclasses import dataclass
@dataclass
class PredictionPipelineConfig:
    prediction_output_dirname:str="predictions" #Prediction results ko save karne ke liye ek folder (predictions) banaya jayega.
    prediction_file_name:str="prediction_file.csv" # Predictions ko ek CSV file me store kiya jayega, jiska naam "prediction_file.csv" hoga.
    model_file_path:str=os.path.join(artifact_folder,'model.pkl')# path to the serialized machine learningmodel
    preprocessor_path:str=os.path.join(artifact_folder,'preprocessor.pkl')# path for the preprocessor used for data transformation
    prediction_file_path:str=os.path.join(prediction_output_dirname,prediction_file_name)# Final prediction file ka complete path banaya gaya ha
class PredictionPipeline:
    def __init__(self,request):
        self.request=request
        self.utils=MainUtils()
        self.prediction_pipeline_config=PredictionPipelineConfig()
    def save_input_files(self)->str:
        # Function ka kaam: User ke diye gaye CSV file ko server pe save karna.
        # Return Type: str → Function ek file path return karega.
        try:
            pred_file_input_dir=self.prediction_pipeline_config.prediction_output_dirname  #Prediction files store karne ke liye ek folder "prediction_artifacts" banaya gaya hai
            os.makedirs(pred_file_input_dir,exist_ok=True)
            input_csv_file=self.request.files['file']#User ka diya CSV file request object se extract kiya gaya hai.
            pred_file_path=os.path.join(pred_file_input_dir,input_csv_file.filename)
            input_csv_file.save(pred_file_path)#User ka uploaded file server pe save kar diya gaya hai.
            return pred_file_path
        except Exception as e:
            raise CustomException(e,sys)
    def predict(self,features):
    # predict function ka kaam hai machine learning model se prediction karna.
        try:
            model=self.utils.load_object(self.prediction_pipeline_config.model_file_path)
            # self.prediction_pipeline_config.model_file_path ek predefined path hai jisme trained model "model.pkl" save hai.
            # self.utils.load_object() ek function hai jo pickle file (.pkl) se model ko load kar raha hai.
            # Iska matlab trained model disk se load ho raha hai, taaki hum usse naye data par predictions le sakein.
            preprocessor=self.utils.load_object(file_path=self.prediction_pipeline_config.preprocessor_path)
            # Pehle jo data transformation hui thi uske liye ek preprocessor object (preprocessor.pkl) save kiya gaya tha.
            # self.utils.load_objects() function us preprocessor ko disk se load kar raha hai.
            # Preprocessor ka kaam hota hai raw input data ko model ke compatible format mein convert karna.
            # Agar preprocessor.pkl ek StandardScaler aur OneHotEncoder ka combination hai, toh yeh naye data par bhi scaling & encoding apply karega.
            if "_id" not in features.columns:
                features["_id"] = 0
            transformed_x=preprocessor.transform(features)
            # preprocessor.transform(features) ka matlab hai ki naye aane wale features ko trained preprocessor ke through transform karna.
            preds=model.predict(transformed_x)
            return preds
        except Exception as e:
            raise CustomException(e,sys)
    def get_predicted_dataframe(self,input_dataframe_path:pd.DataFrame):
        # Yeh function ek CSV file ko input leta hai, uspar prediction karta hai, aur ek naye CSV file me output save karta hai.
        # input_dataframe_path: Yeh ek CSV file ka path hai jo model ke input data ko contain karta hai.
        try:
            prediction_column_name:str=TARGET_COLUMN
            input_dataframe:pd.DataFrame=pd.read_csv(input_dataframe_path)
            if 'unnamed: 0' in input_dataframe.columns:
                input_dataframe = input_dataframe.drop(columns='unnamed: 0', axis=1)
            predictions=self.predict(input_dataframe)
            input_dataframe[prediction_column_name]=[pred for pred in predictions]#Model se jo predictions mile, unko ek naye column me store kiya gaya hai
            target_column_mapping={0:'bad',1:'good'}
            input_dataframe[prediction_column_name]=input_dataframe[prediction_column_name].map(target_column_mapping)
            os.makedirs(self.prediction_pipeline_config.prediction_output_dirname,exist_ok=True)#os.makedirs() ka use karke "predictions" folder banaya ja raha hai, jisme output file store hogi.
            input_dataframe.to_csv(self.prediction_pipeline_config.prediction_file_path,index=False)#Predicted DataFrame ko ek naye CSV file me save kiya ja raha hai.
            logging.info('Prediction completed')
        except Exception as e:
            raise CustomException(e,sys)
    def run_pipeline(self):
        try:
            input_csv_path=self.save_input_files()
        # function user ke upload kiye gaye file ko server ya local directory me save karega.
        # Yeh function file ka path return karega, jisme data saved hai.
            self.get_predicted_dataframe(input_csv_path)
        # Saved CSV file ko read karke us par model se prediction liya ja raha hai.
        # Predictions ko ek naye CSV file me save kiya ja raha hai.
            return self.prediction_pipeline_config
        # PredictionPipelineConfig class ka object return ho raha hai.
        # Isme prediction model ka path, output file ka location aur processor ka path hota hai.
        except Exception as e:
            raise CustomException(e,sys)



