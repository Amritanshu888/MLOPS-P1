## End to End Data Science Project

### Workflows -- ML Pipeline

1. Data Ingestion(Reading some kind of src of data from somewhere it can be a database, API, if an ETL pipeline is basically created most of the times we will be able to fetch some data from some kind of datasource like MySQL, MongoDb and all).
2. Data Validation(Here we need to check the schema of the input we are getting). Whenever we get the new test data to test our model that schema needs to be validated.
3. Data Transformation  ---> We perform Feature Engineering , Data Preprocessing
4. Model Trainer
5. Model Evaluation -> MLFLOW, Dagshub : Go to Dagshub ---> click create ---> there u have a option to connect a repository(bcoz in github i already have my repository)

## The above are 4 major important steps in any End to End Data Science Project
## These modules needs to be created in form of pipeline so that it runs one after the other

## Workflows

1. Update config.yaml   ---> This file is abt some important configurations that we require
2. Update schema.yaml   ---> In case of data validation we need to update this.
3. Update params.yaml   ---> Where i specifically need to provide parameters
4. Update entity        ---> Entire data-ingestion config will be imported over here
5. Update the configuration manager in src config
6. Update the components
7. Update the pipeline  ---> We create two types of pipeline: 1.Training Pipeline 2.Batch Prediction Pipeline
8. Update the main.py