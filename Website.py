import streamlit as st
import pickle 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def load_model():
    with open("rf_regressor_model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

    
def load_data():
    data=pd.read_csv("C:\\Users\\erict\\OneDrive - Asia Pacific University\\Documents\\level 3\\Final Year Project\\dataset and code\\final.csv")
    data['Datetime'] = pd.to_datetime(data['Datetime'])
    data.sort_values('Datetime', inplace=True)
    return data

def Prediction():
    st.title("Application for Predicting Air Quality Index")

    columns = {
        'Sun Hour': float,
        'Heat Index (°C)': int,
        'Wind Gust (Kmph)': int,
        'Cloud Cover': int,
        'Humidity': int,
        'Pressure': int,
        'Temperature (°C)': float,
        'Wind Direction Degree': int,
        'Wind Speed (Kmph)': int,
        'PM2.5 Index': float,
        'PM10 Index': float,
        'NOx Index': float,
        'NH3 Index': float,
        'CO Index': float,
        'SO2 Index': float,
        'O3 Index': float
    }
    
     # Create input fields for each column
    user_inputs = {}
    for column_name, column_type in columns.items():
        if column_type == float:
            user_inputs[column_name] = st.text_input(f"Enter value for {column_name} (float)")
        elif column_type == int:
            user_inputs[column_name] = st.text_input(f"Enter value for {column_name} (integer)")
    
    predict = st.button("Start To Predict")
    if predict:
        # Check if all input fields are filled
        if all(user_inputs.values()):
            # Convert user inputs to a numpy array
            X = np.array([float(user_inputs[column_name]) for column_name in columns.keys()])
            
            # Load the model
            model = load_model()
            
            # Make prediction using the loaded model
            prediction = model.predict(X.reshape(1, -1))
            
            # Display prediction
            st.write("AQI Prediction:",prediction)

        else:
            st.warning("Please fill in all the input fields before predicting.")

def AQI():
    st.title("Explore of AQI")
    data=load_data()
    data.set_index('Datetime', inplace=True)
    data_daily = data.resample('D').mean()
    for year in data_daily.index.year.unique():
        year_data = data_daily[data_daily.index.year == year]
        st.line_chart(year_data['AQI_calculated'], use_container_width=True)

def PM10():
    st.title("Explore of PM10")
    data=load_data()
    data.set_index('Datetime', inplace=True)
    data_daily = data.resample('D').mean()
    for year in data_daily.index.year.unique():
        year_data = data_daily[data_daily.index.year == year]
        st.line_chart(year_data['PM10_SubIndex'], use_container_width=True)

def NOx():
    st.title("Explore of NOx")
    data=load_data()
    data.set_index('Datetime', inplace=True)
    data_daily = data.resample('D').mean()
    for year in data_daily.index.year.unique():
        year_data = data_daily[data_daily.index.year == year]
        st.line_chart(year_data['NOx_SubIndex'], use_container_width=True)



page = st.sidebar.selectbox("Menu",("Prediction","Visualize AQI","Visualize PM10","Visualize NOx"))


if page == "Prediction":
    Prediction()
elif page == "Visualize AQI":
    AQI()
elif page == "Visualize PM10":
    PM10()
elif page == "Visualize NOx":
    NOx()

