#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os


# In[4]:


get_ipython().run_line_magic('pwd', '## To see the present working directory')


# In[5]:


os.chdir("../")  ## This is for going to my parent directory --> i.e. "datascience" project.
get_ipython().run_line_magic('pwd', '')
## After this we will be in our parent directory


# In[6]:


from dataclasses import dataclass
## So i m basically going to create a dataclass
from pathlib import Path

@dataclass ## A decorator
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path
## Same as in config.yaml file
# Difference b/w dataclass and normal class ??
# In normal class most of the times we use self keyword here we don't have to probably use it , and here we are just focused on assigning
# some values to the variable. If u don't have functions at all , then at that time u can use dataclass.
# This Config needs to be passed in the data ingestion pipeline.    


# In[7]:


from src.datascience.constants import * ## import * means everything will be imported from that file , also we can specifically import CONFIG_FILE_PATH
from src.datascience.utils.common import read_yaml, create_directories


# In[8]:


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

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        ## Return type is DataIngestionConfig
        config = self.config.data_ingestion ## bcoz the first key we had in config.yaml was data_ingestion
        create_directories([config.root_dir]) ## first directory we had in data_ingestion was root_dir

        data_ingestion_config = DataIngestionConfig(
            root_dir = config.root_dir,
            source_URL = config.source_URL,
            local_data_file = config.local_data_file,
            unzip_dir = config.unzip_dir
        )
        return data_ingestion_config ## This will be passed to my data ingestion pipeline


# In[10]:


import os
import urllib.request as request
from src.datascience import logger
import zipfile


# In[15]:


## Data Ingestion Component
class DataIngestion:
    def __init__(self,config:DataIngestionConfig): ## Return type of config will be DataIngestionConfig
        self.config = config ## assigning config
    
    ## Downloading the zip file
    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(  ## Whe we do url retriever we have to load the data into my local_data_file
                url = self.config.source_URL,
                filename = self.config.local_data_file    ## These are available in config/config.yaml , at this path my entire file will get created
            )
            logger.info(f"{filename} download! with following info: \n{headers}")
        else:
            logger.info(f"File already exists")

    ## Extract the zip file
    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function retuns None
        """ 
        unzip_path = self.config.unzip_dir ## On this path the entire zip file will be unzipped
        os.makedirs(unzip_path,exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file,'r') as zip_ref:
            zip_ref.extractall(unzip_path)      


# In[ ]:


try:
   config = ConfigurationManager()
   data_ingestion_config = config.get_data_ingestion_config() ## get_data_ingestion_config is taking out all the information
   data_ingestion = DataIngestion(config=data_ingestion_config)
   data_ingestion.download_file()
   data_ingestion.extract_zip_file()
except Exception as e:
   raise e  

## Note: If params.yaml or schema.yaml is empty it will throw the error : so add anything in them , like for eg. key: value(for rightnow)
# After this ur artifacts folder will be created.
# Now we will do the same as we have done here , just we will do in modular coding 

