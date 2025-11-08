## We are creating a basic frontend over here(basically a flask api so that i integrate this prediction pipeline along with this).
from flask import Flask,render_template,request
import os
import numpy as np
import pandas as pd
from src.datascience.pipeline.prediction_pipeline import PredictionPipeline

app = Flask(__name__) ## This is basically my app w.r.t flask

@app.route('/',methods=['GET']) ## route to display the home page
def homepage():
    return render_template("index.html")  ## This index.html should be created inside the template folder in our directory

@app.route('/train',methods=['GET']) ## route to the train the pipeline
def training():
    ## Inside this function i have to execute my main.py file because there i have my entire training pipeline.
    os.system("python main.py") ## So it is just going to execute this command
    return "Training Successfull"

@app.route('/predict',methods=['POST','GET']) ## route from web ui
def index():
    if request.method == 'POST':
        ## If its a POST that means that we are submitting some information. Basically we are checking a condition here.
        try:
            ## Inside this try block i will read the inputs given by the user
            fixed_acidity = float(request.form['fixed_acidity']) ## It will go to index.html and read the label('fixed_acidity').
            volatile_acidity = float(request.form['volatile_acidity'])
            citric_acid = float(request.form['citric_acid'])
            residual_sugar = float(request.form['residual_sugar'])
            chlorides = float(request.form['chlorides'])
            free_sulphur_dioxide = float(request.form['free_sulphur_dioxide'])
            total_sulphur_dioxide = float(request.form['total_sulphur_dioxide'])
            density = float(request.form['density'])
            pH = float(request.form['pH'])
            sulphates = float(request.form['sulphates'])
            alcohol = float(request.form['alcohol'])   ## All these fields are present in index.html form in input tag id.

            ## Take all these data and combine them into a list
            data = [fixed_acidity,volatile_acidity,citric_acid,residual_sugar,chlorides,free_sulphur_dioxide,
                    total_sulphur_dioxide,density,pH,sulphates,alcohol]
            
            ## Now i have to reshape this data, i m putting the data in list , so i will reshape them in one row with eleven columns
            data = np.array(data).reshape(1,11) ## Here we will call it as a one exact row.

            ## Now we will call our prediction pipeline
            obj = PredictionPipeline()
            predict = obj.predict(data)

            return render_template('results.html',prediction=str(predict)) ## Whatever output i m getting i m converting it to a string.
            ## 'predict' is the value that i m passing to my results.html
        except Exception as e:
            return "Something is wrong"

    ## If its a 'GET' request
    else:
        return render_template('index.html') ## Here we don't need to pass any information

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)            

## To run this app : Terminal me --> python app.py
## To start the training : URL ke top pe : /train ---> To start the training
## From the web ui itself i m able to train my model by calling /train ---> which is running python main.py where our training pipeline code is written.
