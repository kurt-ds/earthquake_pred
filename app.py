from flask import Flask, request, render_template
import pickle
import numpy as np
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))

def convert_to_24h_int(time_str):
    # Split the hours and minutes from the string
    hours, minutes = map(int, time_str.split(":"))

    # Convert the time to 24-hour format integer
    total_minutes = (hours * 60) + minutes
    return total_minutes

def getClass(richter_value):
    intensity_scale = {
        0: "micro",
        1: "minor",
        2: "light",
        3: "moderate",
        4: "strong",
        5: "major",
        6: "great"
    }

    # Check if value is within valid Richter scale range (0 to 9)
    if 0 <= richter_value <= 9:
        return intensity_scale.get(richter_value)  # Use get() to handle missing values
    else:
        return "Invalid Richter value"

# Load earthquake data from CSV file
earthquake_data = pd.read_csv("earthquake_dataset.csv")

# Create a new column 'DateTime' in the desired format
earthquake_data['DateTime'] = (' Date: ' + earthquake_data['Day'].astype(str) + '/' + 
                               earthquake_data['Month'].astype(str) + '/' + 
                               earthquake_data['Year'].astype(str))

@app.route('/')
def index():
    richter_data = [
        {"magnitude": "less than 1.0 to 2.9", "category": "micro", "effects": "generally not felt by people, though recorded on local instruments", "per_year": "more than 100,000"},
        {"magnitude": "3.0-3.9", "category": "minor", "effects": "felt by many people; no damage", "per_year": "12,000–100,000"},
        {"magnitude": "4.0-4.9", "category": "light", "effects": "felt by all; minor breakage of objects", "per_year": "2,000–12,000"},
        {"magnitude": "5.0-5.9", "category": "moderate", "effects": "some damage to weak structures", "per_year": "200–2,000"},
        {"magnitude": "6.0-6.9", "category": "strong", "effects": "moderate damage in populated areas", "per_year": "20–200"},
        {"magnitude": "7.0-7.9", "category": "major", "effects": "serious damage over large areas; loss of life", "per_year": "3–20"},
        {"magnitude": "8.0 and higher", "category": "great", "effects": "severe destruction and loss of life over large areas", "per_year": "fewer than 3"},
    ]

    # Density Mapbox
    # fig = px.density_mapbox(earthquake_data, lat='Latitude', lon='Longitude',
    #                         z='Richter Category', radius=4, hover_name='DateTime',
    #                         title='Philippine Seismic Activity Map (2018-2024)',
    #                         zoom=4.25)
    
    # Scatter Mapbox
    fig = px.scatter_mapbox(earthquake_data, lat='Latitude', lon='Longitude',
                            color='Richter Category',
                            animation_frame='DateTime',
                            height=900,
                            animation_group='Richter Category',
                            size='Magnitude',
                            hover_name='DateTime',
                            title='Philippine Seismic Activity Map (2018-2024)',
                            zoom=3.75,
                            color_discrete_sequence=["fuchsia"]) 

    fig.update_layout(
        mapbox_style="open-street-map",
        height=600,
        margin={"r": 50, "t": 100, "l": 50, "b": 50},
    )

    fig_container = fig.to_html(full_html=False)    
    return render_template('earthquake.html', richter_data=richter_data, fig=fig_container)

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    richter_data = [
        {"magnitude": "less than 1.0 to 2.9", "category": "micro", "effects": "generally not felt by people, though recorded on local instruments", "per_year": "more than 100,000"},
        {"magnitude": "3.0-3.9", "category": "minor", "effects": "felt by many people; no damage", "per_year": "12,000–100,000"},
        {"magnitude": "4.0-4.9", "category": "light", "effects": "felt by all; minor breakage of objects", "per_year": "2,000–12,000"},
        {"magnitude": "5.0-5.9", "category": "moderate", "effects": "some damage to weak structures", "per_year": "200–2,000"},
        {"magnitude": "6.0-6.9", "category": "strong", "effects": "moderate damage in populated areas", "per_year": "20–200"},
        {"magnitude": "7.0-7.9", "category": "major", "effects": "serious damage over large areas; loss of life", "per_year": "3–20"},
        {"magnitude": "8.0 and higher", "category": "great", "effects": "severe destruction and loss of life over large areas", "per_year": "fewer than 3"},
    ]

    date = request.form.get('Date')
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    day = int(date_obj.day)
    month = int(date_obj.month)
    year = int(date_obj.year)

    time = request.form.get('Time')
    time = int(convert_to_24h_int(time))

    latitude = round(float(request.form.get('Latitude')), 2)
    longitude = round(float(request.form.get('Longitude')), 2)

    zipcode = int(request.form.get('Zipcode'))

    new_data = [day, month, year, time, latitude, longitude, zipcode]
    feature_names = ['Day', 'Month', 'Year', 'Time', 'Latitude', 'Longitude', 'Zip Code']
    to_pred = pd.DataFrame(data=[new_data], columns=feature_names)
    prediction = model.predict(to_pred)[0]
    category = getClass(prediction)

    df = pd.DataFrame({
        'Day': [day],
        'Month': [month],
        'Time': [time],
        'Year': [year],
        'Latitude': [latitude],
        'Longitude': [longitude],
        'Zipcode': [zipcode],
        'Richter Category': [category]
    })

    fig = px.scatter_mapbox(df, lat='Latitude', lon='Longitude',
                            color='Richter Category',
                            title='Philippine Earthquake Prediction Map',
                            zoom=12,
                            color_discrete_sequence=["fuchsia"])

    fig.update_layout(
        mapbox_style="open-street-map",
        height=600,
        margin={"r": 50, "t": 100, "l": 50, "b": 50},
        legend_title_text='Category using Richter Scale',title_font_size=40, title_y=0.97
    )

    fig_container = fig.to_html(full_html=False)

    if (len(category) > 8):
        return render_template('earthquake.html', pred=category, richter_data=richter_data, fig=fig_container)
    else:
        return render_template('earthquake.html', pred=category, richter_data=richter_data, fig=fig_container)

if __name__ == '__main__':
    app.run(debug=True)