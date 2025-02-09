import sys
import os
import pandas as pd
import numpy as np
from typing import Generator,List,Tuple
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from sklearn.model_selection import train_test_split,GridSearchCV
from src.constant import *
from src.exception import CustomException
from src.logger import logging
from src.utils.main_utils import MainUtils
from dataclasses import dataclass
@dataclass
class ModelTrainerConfig:
    artifact_folder=os.path.join(artifact_folder)
    trained_model_path=os.path.join(artifact_folder,'model.pkl')
    expected_accuracy=0.45
    model_config_file_path=os.path.join('config','model.yaml')
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()
        self.utils=MainUtils()
        self.models={
            "XGBClassifier":XGBClassifier(),
            'GradientBoostingClassifier':GradientBoostingClassifier(),
            'SVC':SVC(),
            'RandomForestClassifier':RandomForestClassifier()
        }
    def get_model(self,x,y,models):
        try:
            x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=1)
            report={}
            # har model ke liye traininh hogi
            for i,j in models.items():
                # i is for keys anf j is for values
                j.fit(x_train,y_train)
                y_train_pred=j.predict(x_train)
                y_test_pred=j.predict(x_test)
                train_model_score=accuracy_score(y_train,y_train_pred)
                test_model_score=accuracy_score(y_test,y_test_pred)
                report[i]=test_model_score
            #best model chahiye
            best_model_name=max(report,key=report.get)
            # report.get(key) Python में dictionary की एक method है, जो dictionary से दिए गए key का value return करता है।
            best_model_score=report[best_model_name]
            best_model_object=models[best_model_name]
            return best_model_name,best_model_object,best_model_score,report
        except Exception as e:
            raise CustomException(e,sys)
    # Finetune method me
    # Finetune method me
    def finetune_best_model(self, best_model_object: object, best_model_score, x_train, y_train) -> object:
        try:
            # Read the config YAML file
            model_param_grid = self.utils.read_yaml_file(self.model_trainer_config.model_config_file_path)
            print("model_param_grid:", model_param_grid)  # Print to debug
            
            # Access the model parameter grid using 'model_selection' key
            for model_name, params in model_param_grid['model_selection']['model'].items():
                for param_name, param_values in params['search_param_grid'].items():
                    if not isinstance(param_values, list):
                        model_param_grid['model_selection']['model'][model_name]['search_param_grid'][param_name] = [param_values]

            # Now perform GridSearchCV
            grid_search = GridSearchCV(best_model_object, param_grid=model_param_grid['model_selection']['model'][best_model_object.__class__.__name__]['search_param_grid'], cv=5, n_jobs=-1)
            grid_search.fit(x_train, y_train)

            best_param = grid_search.best_params_
            print('best_params are', best_param)
            finetuned_model = best_model_object.set_params(**best_param)

            return finetuned_model
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info(f"bhai model traning mein initiate wale function ke andar hai")
            x_train = train_array[:, :-1]  # All columns except the last one
            y_train = train_array[:, -1]   # Last column is the target
            x_test=test_array[:, :-1]
            y_test=test_array[:, -1]
            best_model_name,best_model_object,best_model_score,model_report= self.get_model(x=x_train,y=y_train,models=self.models)
            print(model_report)
            best_model=self.finetune_best_model(best_model_object=best_model_object,best_model_score=best_model_score,x_train=x_train,y_train=y_train)
            best_model.fit(x_train,y_train)
            y_pred=best_model.predict(x_test)
            test_accuracy_score=accuracy_score(y_test,y_pred)
            if test_accuracy_score<.5:
                raise Exception("No best model found with accuracy 0.6")
            logging.info(f"best found model on both training and testing dataset")
            logging.info(f"saving model at path:{self.model_trainer_config.trained_model_path}")
            os.makedirs(os.path.dirname(self.model_trainer_config.trained_model_path),exist_ok=True)
            # os.path.dirname() ka kaam hota hai kisi given file path se directory ka path nikaalna.
            # os.makedirs() ka kaam hota hai specified path par directory create karna
            self.utils.save_object(
                file_path=self.model_trainer_config.trained_model_path,
                obj=best_model
            )
            return self.model_trainer_config.trained_model_path,test_accuracy_score
        except Exception as e:
            raise CustomException(e,sys)
    # def finetune_best_model(self,best_model_object:object,best_model_score,x_train,y_train)-> object:
    #     try:
    #         model_param_grid=self.utils.read_yaml_file(self.model_trainer_config.model_config_file_path)
    #         grid_search=GridSearchCV(best_model_object,param_grid=model_param_grid,cv=5,n_jobs=-1)
    #         grid_search.fit(x_train,y_train)
    #         best_param=grid_search.best_params_
    #         print('best_params are',best_param)
    #         finetuned_model=best_model_object.set_params(**best_param)
    #         return finetuned_model
    #     except Exception as e:
    #         raise CustomException(e,sys)







    


    

