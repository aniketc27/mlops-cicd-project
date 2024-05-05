import pickle
import io
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify,send_file,Response
from joblib import load
import os

app = Flask(__name__)

# Load the pre-trained machine learning model
MODEL_DIR = os.environ["MODEL_DIR"]
model_file = 'light_model.joblib'
model_path = os.path.join(MODEL_DIR, model_file)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # print('Classifier Santander Usecase')
        # Get the CSV file from the request
        file = request.files['file']
        # print('file read')
        # Read the CSV file into a pandas DataFrame
        data = pd.read_csv(file)

        df = data['ID_code']
        data = data.drop('ID_code',axis =1)
        # print('Data read')
        
        model = load(model_path)      
        # Make predictions using the pre-trained model
        predictions = model.predict(data)
        
        pred_class  = np.where(predictions >0.5, "1", "0") 
        predictions = pd.DataFrame(pred_class, columns=['Prediction'])
        df = pd.concat([df,predictions], axis = 1)

        # print(df.head())
        # print('predictions done')

        return jsonify(df.to_dict(orient='records')),200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True , port=5001)
