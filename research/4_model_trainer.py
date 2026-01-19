#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os


# In[2]:


get_ipython().run_line_magic('pwd', '')


# In[3]:


os.chdir("../") ## This means os.change_directory to my root


# In[4]:


get_ipython().run_line_magic('pwd', '## To get presentP(p) working(w) directroy(d)')


# In[ ]:


from dataclasses import dataclass
from pathlib import Path

@dataclass
class ModelTrainerConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    model_name: str
    alpha: float    ## Why alpha ?? ----> As in this project i m going to apply Elastic-Net ML Algo. Inside that we have two parameters : alpha and l1_ratio
    l1_ratio: float
    target_column: str


# In[6]:


## The above parameters : alpha and l1_ratio will be specified in params.yaml file.
## Further in parameters we will assign multiple values and then we will do hyperparameter-tuning on those parameters.

from src.datascience.constants import *
from src.datascience.utils.common import read_yaml, create_directories


# In[11]:


class ConfigurationManager:
    def __init__(self,
    config_filepath = CONFIG_FILE_PATH,
    params_filepath = PARAMS_FILE_PATH,
    schema_filepath = SCHEMA_FILE_PATH):

       self.config = read_yaml(config_filepath)
       self.params = read_yaml(params_filepath)
       self.schema = read_yaml(schema_filepath)

       create_directories([self.config.artifacts_root])

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer ## This is present in key-value format in config.yaml file
        params = self.params.ElasticNet
        schema = self.schema.TARGET_COLUMN ## This is present in schema.yaml file

        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir = config.root_dir,
            train_data_path = config.train_data_path,
            test_data_path = config.test_data_path,
            model_name = config.model_name,
            alpha = params.alpha,
            l1_ratio = params.l1_ratio,
            target_column = schema.name   ## Name of the target column
        )

        return model_trainer_config


# In[12]:


import pandas as pd
import os
from src.datascience import logger
from sklearn.linear_model import ElasticNet
import joblib


# In[13]:


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train(self):
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)

        train_x = train_data.drop([self.config.target_column], axis=1)
        test_x = test_data.drop([self.config.target_column], axis=1)
        train_y = train_data[[self.config.target_column]]
        test_y = test_data[[self.config.target_column]]

        lr = ElasticNet(alpha = self.config.alpha, l1_ratio = self.config.l1_ratio, random_state = 42)
        lr.fit(train_x,train_y)

        joblib.dump(lr, os.path.join(self.config.root_dir,self.config.model_name))    


# In[14]:


try:
    config = ConfigurationManager()
    model_trainer_config = config.get_model_trainer_config()
    model_trainer = ModelTrainer(config=model_trainer_config)
    model_trainer.train()
except Exception as e:
    raise e    

