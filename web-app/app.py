import pickle
import io
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify,send_file,Response

app = Flask(__name__)

# Load the pre-trained machine learning model
model = pickle.load(open('lgbm.pkl', 'rb'))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        print('Classifier Santander Usecase')
        # Get the CSV file from the request
        file = request.files['file']
        
        # Read the CSV file into a pandas DataFrame
        data = pd.read_csv(file)

        df = data['ID_code']
        data = data.drop('ID_code',axis =1)
        print('Data read')
                
        # Make predictions using the pre-trained model
        predictions = model.predict(data)
        
        pred_class  = np.where(predictions >0.5, "1", "0") 
        predictions = pd.DataFrame(pred_class, columns=['Prediction'])
        data = pd.concat([data, predictions], axis =1)
        df = pd.concat([df,data], axis = 1)

        print(df.head())
        print('predictions done')

        csv_data = df.to_csv(index=False)
        csv_file = io.StringIO(csv_data)
        g=file(csv_file)
        return Response(g, direct_passthrough=True)
        # Create a BytesIO object to store the CSV data
        output = io.BytesIO()
        output.write(csv_data.encode('utf-8'))
        output.seek(0)
        
        # Return the CSV file as a response
        # return send_file(
        #     output,
        #     mimetype='text/csv',
        #     # attachment_filename='predictions.csv',
        #     download_name = 'predictions.csv',
        #     as_attachment=True)
        # return jsonify(df.to_dict(orient='records')),200#fix this add error handling

        
        # Create a file-like object from the CSV data
        # csv_file = io.StringIO(csv_data)
        
        # # Stream CSV file as response
        # return Response(
        #     csv_generator(csv_file),
        #     mimetype='text/csv',
        #     headers={'Content-Disposition': 'attachment; filename=predictions.csv'}
        # )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def csv_generator(csv_file):
    # Generate CSV data in chunks
    while True:
        chunk = csv_file.read(4096)
        if not chunk:
            break
        yield chunk

if __name__ == '__main__':
    app.run(debug=True)
