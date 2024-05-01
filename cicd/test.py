import pandas as pd
import numpy as np
from joblib import load
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score
import lightgbm as lgb
import xgboost as xgb
import pickle
import json
import os

# Set path for the input (model)
MODEL_DIR = os.environ["MODEL_DIR"]
#MODEL_DIR = '.\cicd\\model'
model_file = 'light_model.joblib'
model_path = os.path.join(MODEL_DIR, model_file)

# Set path for the input (test data)
PROCESSED_DATA_DIR = os.environ["PROCESSED_DATA_DIR"]
#PROCESSED_DATA_DIR = '.\cicd\\processed_data'
test_data_file = 'test.csv'
test_data_path = os.path.join(PROCESSED_DATA_DIR, test_data_file)

# Load model
light_model = load(model_path)

# Load data
df = pd.read_csv(test_data_path, sep=",")
df = df.drop('ID_code',axis =1)

# Split data into dependent and independent variables
X_test = df.drop('target', axis=1)
y_test = df['target']

predictions = np.zeros(len(X_test))

# Predict
predictions = light_model.predict(X_test)
predictions = pd.Series(predictions)

# Compute test accuracy

test_logit = accuracy_score(y_test,(predictions>0.5))

#Test accuracy to JSON
test_metadata = {
    'test_acc': test_logit
}

# Set output path
RESULTS_DIR = os.environ["RESULTS_DIR"]
#RESULTS_DIR='.\cicd\\results'
test_results_file = 'test_metadata.json'
results_path = os.path.join(RESULTS_DIR, test_results_file)

# Serialize and save metadata
with open(results_path, 'w') as outfile:
    json.dump(test_metadata, outfile)
print('Accuracy ',test_logit)
print('Testing complete')