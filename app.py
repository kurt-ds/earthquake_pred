from flask import Flask,request, url_for, redirect, render_template
import pickle
import numpy as np
from datetime import datetime

app = Flask(__name__)

model=pickle.load(open('model.pkl','rb'))

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


@app.route('/')
def hello_world():
    return render_template("earthquake.html")


@app.route('/predict',methods=['POST','GET'])
def predict():
    date = request.form.get('Date')
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    day = int(date_obj.day)
    month = int(date_obj.month)

    time = request.form.get('Time')
    time = int(convert_to_24h_int(time))

    latitude = round(float(request.form.get('Latitude')), 2)
    longitude = round(float(request.form.get('Longitude')), 2)

    zipcode = int(request.form.get('Zipcode'))

    new_data = [day, month, time, latitude, longitude, zipcode]

    prediction = model.predict([new_data])[0]

    category = getClass(prediction)


    if (len(category) > 8):
       return render_template('earthquake.html', pred=category)
    else:
       return render_template('earthquake.html', pred=f"Your earthquake category is: {category}")


if __name__ == '__main__':
    app.run(debug=True)