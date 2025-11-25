from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Load the model
MODEL_PATH = 'pet_suggestion_model.pkl'
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None
    print(f"Warning: Model file not found at {MODEL_PATH}")

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        data = request.get_json()
        
        # Expected keys: Name, Gender, Age, Salary, Mental Condition, Allergies, Satisfaction
        # Note: 'Name' and 'Satisfaction' might not be used by the model but are in the CSV.
        # We need to match the columns the model expects.
        # Based on model_training.py, the features are:
        # ['Gender', 'Age', 'Salary', 'Mental Condition', 'Allergies']
        
        # Create a DataFrame from the input
        # We need to ensure we provide all columns expected by the pipeline
        
        input_data = pd.DataFrame([data])
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        
        return jsonify({
            'recommended_pet': prediction,
            'input_received': data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
