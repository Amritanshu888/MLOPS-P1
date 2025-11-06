from src.datascience import logger ## This logger is present in __init__.py
from src.datascience.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.datascience.pipeline.data_validation_pipeline import DataValidationTrainingPipeline
from src.datascience.pipeline.data_transformation_pipeline import DataTransformationTrainingPipeline
from src.datascience.pipeline.model_trainer_pipeline import ModelTrainerTrainingPipeline
from src.datascience.pipeline.model_evaluation_pipeline import ModelEvaluationTrainingPipeline

logger.info("Welcome to our custom logging data science")  ## Some message here

## In terminal
## python main.py ----> pycache folder will be created carrying details , logs folder will be created and there a file name logging.log will be their(as specified by us in src/datascience/__init__.py) carrying the details.
## Exception Handling is implemented with the help of python-box.

STAGE_NAME = "Data Ingestion stage"
try:
    logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.initiate_data_ingestion()
    logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<\n\nx======x")
except Exception as e:
    logger.exception(e)
    raise e

## Execute in terminal python main.py    

#[2025-10-17 15:40:14,408: INFO: main: >>>>> stage Data Ingestion stage started <<<<<]
#[2025-10-17 15:40:14,409: INFO: common: yaml file: config\config.yaml loaded successfully]
#[2025-10-17 15:40:14,410: INFO: common: yaml file: params.yaml loaded successfully]
#[2025-10-17 15:40:14,410: INFO: common: yaml file: schema.yaml loaded successfully]
#[2025-10-17 15:40:14,411: INFO: common: Created directory at: artifacts]
#[2025-10-17 15:40:14,411: INFO: common: Created directory at: artifacts/data_ingestion]
#[2025-10-17 15:40:14,411: INFO: data_ingestion: File already exists]
#[2025-10-17 15:40:14,413: INFO: main: >>>>> stage Data Ingestion stage completed <<<<<

#x======x]

## Output which we are getting : Timestamp bcoz everything is getting logged

STAGE_NAME = "Data Validation stage"
try:
    logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
    data_ingestion = DataValidationTrainingPipeline()
    data_ingestion.initiate_data_validation()
    logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<\n\nx=========x")
except Exception as e:
    logger.exception(e)
    raise e  

## Test it : python main.py -----> execute this in terminal

STAGE_NAME = "Data Transformation stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    data_ingestion = DataTransformationTrainingPipeline()
    data_ingestion.initiate_data_transformation()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<<<\n\nx===========x")
except Exception as e:
    logger.exception(e)
    raise e  

STAGE_NAME = "Model Trainer stage"
try:
    logger.info(f">>>>> stage {STAGE_NAME} started <<<<<<")
    data_ingestion = ModelTrainerTrainingPipeline()
    data_ingestion.initiate_model_training()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<<<\n\nx========x")
except Exception as e:
    logger.exception(e)
    raise e   

STAGE_NAME = "Model evaluation stage"
try:
    logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
    data_ingestion = ModelEvaluationTrainingPipeline()
    data_ingestion.initiate_model_evaluation()
    logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<<\n\nx===========x")
except Exception as e:
    logger.exception(e)
    raise e    

