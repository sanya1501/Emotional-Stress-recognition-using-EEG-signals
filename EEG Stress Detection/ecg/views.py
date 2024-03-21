# ecg/views.py
from django.shortcuts import render, redirect
from .models import ECGRecord
import random
import string
import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pd

# Step 1: Data Preprocessing
# Load the dataset
df = pd.read_excel("./dataset/dataset.xlsx")
# Drop irrelevant columns
df.drop(["Subject", "timestamps"], axis=1, inplace=True)
# Check for missing values and handle if necessary
if df.isnull().sum().any():
    df.fillna(0, inplace=True)  # Replace missing values with 0 or apply any other suitable strategy
# Encode the "Emotion" labels into numerical values
label_encoder = LabelEncoder()
df["Emotion"] = label_encoder.fit_transform(df["Emotion"])
# Split the dataset into features (X) and labels (y)
X = df.drop("Emotion", axis=1)
y = df["Emotion"]

# Step 3: Feature Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

def home(request):
    if request.method == 'POST':
        tp9 = request.POST.get('tp9', 0)
        tp10 = request.POST.get('tp10', 0)
        af8 = request.POST.get('af8', 0)
        af7 = request.POST.get('af7', 0)
        right_aux = request.POST.get('right_aux', 0)

        # Calculate the sum of inputs
        total_sum = tp9 + tp10 + af8 + af7 + right_aux

        # Load the SVM model from the file
        model_filename = "./model/svm_model.pkl"
        loaded_svm_model = joblib.load(model_filename)

        # Input data for testing
        input_data = np.array([[tp9 , af7 , af8 , tp10 , right_aux]])

        # Feature scaling for the input data (using the same scaler as before)
        input_data_scaled = scaler.transform(input_data)

        # Make predictions using the loaded SVM model
        predicted_emotion = loaded_svm_model.predict(input_data_scaled)

        # Convert numerical label back to emotion category using the label_encoder
        predicted_emotion_category = label_encoder.inverse_transform(predicted_emotion)

        output = predicted_emotion_category[0]

        # Save the input and output to the database
        ECGRecord.objects.create(tp9=tp9, tp10=tp10, af8=af8, af7=af7, right_aux=right_aux, output=output)

        return redirect('history')  # Redirect to the history page after submitting the form

    return render(request, 'home.html')

def history(request):
    records = ECGRecord.objects.all().order_by('-id')


    return render(request, 'history.html', {'records': records})

def main(request):

    return render(request, 'index.html')
