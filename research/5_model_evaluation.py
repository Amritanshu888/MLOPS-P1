#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
os.environ["MLFLOW_TRACKING_URI"] = "https://dagshub.com/amritanshubhardwaj12crosary/MLOPS-P1.mlflow"
os.environ["MLFLOW_TRACKING_USERNAME"] = "amritanshubhardwaj12crosary"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "0fb168e7cb38689121e16da0859f210fbc442180" ## Remote -> Data -> DVC -> Credentials -> Secret Access Key


# - From the above setup anything that u will track will be tracked in ur Dagshub Remote Repository

# In[2]:


import os
get_ipython().run_line_magic('pwd', '')


# In[3]:


os.chdir("../")
get_ipython().run_line_magic('pwd', '')


# In[4]:


from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    test_data_path: Path
    model_path: Path
    all_params: dict
    metric_file_name: Path
    target_column: str
    mlflow_uri: str


# In[6]:


from src.datascience.constants import *
from src.datascience.utils.common import read_yaml, create_directories, save_json


# In[7]:


class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH,
        schema_filepath = SCHEMA_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        create_directories([self.config.artifacts_root])

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config.model_evaluation
        params = self.params.ElasticNet
        schema = self.schema.TARGET_COLUMN

        create_directories([config.root_dir])

        model_evaluation_config = ModelEvaluationConfig(
            root_dir = config.root_dir,
            test_data_path = config.test_data_path,
            model_path = config.model_path,
            all_params = params,
            metric_file_name = config.metric_file_name,
            target_column = schema.name,
            mlflow_uri = "https://dagshub.com/amritanshubhardwaj12crosary/MLOPS-P1.mlflow"
        )
        return model_evaluation_config    


# In[8]:


import os
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import numpy as np
import joblib


# In[9]:


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metric(self,actual,pred):
        rmse = np.sqrt(mean_squared_error(actual,pred))
        mae = mean_absolute_error(actual,pred)
        r2 = r2_score(actual,pred)
        return rmse, mae, r2

    def log_into_mlflow(self):
        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        test_x = test_data.drop([self.config.target_column], axis = 1)
        test_y = test_data[[self.config.target_column]]

        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():
            predicted_qualities = model.predict(test_x)

            (rmse, mae, r2) = self.eval_metric(test_y, predicted_qualities)

            ## Saving metrics as local
            scores = {"rmse":rmse, "mae":mae, "r2":r2}
            save_json(path=Path(self.config.metric_file_name), data=scores)

            mlflow.log_params(self.config.all_params)

            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("r2", r2)
            mlflow.log_metric("mae", mae)

            # Model registry does not work with file store
            if tracking_url_type_store != "file":
                ## Register the model
                # There are other ways to use the Model Registry, which depends on the use case,
                # please refer to the doc for more information:
                # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                mlflow.sklearn.log_model(model,"model",registered_model_name="ElasticnetModel")
            else:
                mlflow.sklearn.log_model(model,"model")            


# In[10]:


try:
    config = ConfigurationManager()
    model_evaluation_config = config.get_model_evaluation_config()
    model_evaluation = ModelEvaluation(config = model_evaluation_config)
    model_evaluation.log_into_mlflow()
except Exception as e:
    raise e    


# - After this u can go to that project's repo(on dagshub) and see experiments.
# - From experiments we can also go to MLFLOW UI.
