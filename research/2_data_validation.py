#!/usr/bin/env python
# coding: utf-8

# In[4]:


import os


# In[5]:


get_ipython().run_line_magic('pwd', '')


# In[6]:


os.chdir("../")
get_ipython().run_line_magic('pwd', '')


# In[7]:


import pandas as pd

data = pd.read_csv("artifacts/data_ingestion/winequality-red.csv")
data.head()
## Quality is the output feature here.


# In[8]:


## Now we have to define our schema
data.info()


# - Why we require this above bcoz we have something called as schema.yaml
# - In schema.yaml put the above info.

# In[9]:


data.isnull().sum()


# In[10]:


data.shape


# In[11]:


from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: str
    unzip_data_dir: Path
    all_schema: dict ## This will have all the schema details which we are reading from schema.yaml file. ---> This will hold the entire schema.yaml


# In[12]:


from src.datascience.constants import *
from src.datascience.utils.common import read_yaml, create_directories


# In[13]:


class ConfigurationManager:
    def __init__(self,
                 config_filepath=CONFIG_FILE_PATH,
                 params_filepath=PARAMS_FILE_PATH,
                 schema_filepath=SCHEMA_FILE_PATH):  ## This CONFIG_FILE_PATH will be defined in : src/constants
        ## The above is basically my constructor for this particular class
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        ## First folder getting created here in config.yaml is artifacts folder
        create_directories([self.config.artifacts_root]) ## artifacts folder will be created

    def get_data_validation_config(self) -> DataValidationConfig:
        config =  self.config.data_validation   ## Data Validation wala config
        schema = self.schema.COLUMNS

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir = config.root_dir,
            STATUS_FILE = config.STATUS_FILE,
            unzip_data_dir = config.unzip_data_dir,
            all_schema = schema
        )

        return data_validation_config


# In[14]:


import os
from src.datascience import logger


# In[15]:


## After we read the dataset we need to compare it with the schema and then set the status whether its ok or not.
class DataValidation:
    def __init__(self,config: DataValidationConfig): ## These are the parameters passed
        self.config = config

    def validate_all_columns(self)-> bool:
        try:
            validation_status = None

            data = pd.read_csv(self.config.unzip_data_dir)
            all_cols = list(data.columns)

            all_schema = self.config.all_schema.keys()

            for col in all_cols:
                if col not in all_schema:
                    validation_status = False
                    with open(self.config.STATUS_FILE,'w') as f:
                        f.write(f"Validation status: {validation_status}")
                else:
                    validation_status = True
                    with open(self.config.STATUS_FILE,'w') as f:
                        f.write(f"Validation status: {validation_status}")

            return validation_status

        except Exception as e:
            raise e                        


# In[17]:


try:
    config = ConfigurationManager()
    data_validation_config = config.get_data_validation_config()
    data_validation = DataValidation(config=data_validation_config)
    data_validation.validate_all_columns()
except Exception as e:
    raise e    

