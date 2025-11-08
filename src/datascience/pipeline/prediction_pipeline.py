## Here our main task is to load the model and do the prediction.
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

class PredictionPipeline:
    def __init__(self):
        self.model = joblib.load(Path('artifacts/model_trainer/model.joblib'))

    def predict(self,data):
        prediction = self.model.predict(data)

        return prediction

## Now we also know that we have to create a frontend UI --> Then try to include this prediction pipeline directly from that frontend ui.
# Next we go to app.py        