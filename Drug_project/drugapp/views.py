# myapp/views.py
import os
from django.shortcuts import render
from django.http import HttpResponse
import pickle
import numpy as np
from sklearn.preprocessing import OneHotEncoder

def homepage(request):
    return render(request, "index.html")

def predict(request):
    if request.method == 'POST':
        try:
            # reading the inputs given by the user
            gender = int(request.POST['gender'])
            age = int(request.POST['age'])
            bp = request.POST['bp']
            cholesterol = request.POST['cholesterol']
            na_to_k = int(request.POST['na_to_k'])

            inPut = np.array([[gender, age, bp, cholesterol, na_to_k]])
            print(inPut)
            
            # Load the scaler using joblib
            #scaler = joblib.load('finalEncoder.pkl')
            scaler = pickle.load(open('drugapp/final_Scaler.pkl','rb'))

            # Load the model using joblib
            #model = joblib.load('finalModel.pkl')
            model = pickle.load(open('drugapp/final_Model.pkl', 'rb'))
            # Transform input data using the loaded scaler
            #encoder = OneHotEncoder(handle_unknown='ignore')
            scaler_data = scaler.transform(inPut)


            # Make predictions using the loaded model
            prediction = model.predict(scaler_data)

            # Showing the prediction results in a UI
            return render(request, 'results.html', {'prediction': prediction[0]})
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            return render(request, 'error.html', {'error_message': 'An error occurred. Please try again.'})
            return HttpResponse('Something went wrong')
    else:
        return render(request, 'index.html')
