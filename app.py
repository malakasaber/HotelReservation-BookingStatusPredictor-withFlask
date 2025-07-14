from flask import Flask, render_template, request
import pickle
import numpy as np
from datetime import datetime

app = Flask(__name__)

# Load trained model and scaler
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None

    if request.method == 'POST':
        try:
            input_data = [
                float(request.form['number_of_adults']),
                float(request.form['number_of_children']),
                float(request.form['number_of_weekend_nights']),
                float(request.form['number_of_week_nights']),
                encode_meal(request.form['type_of_meal']),
                float(request.form['car_parking_space']),
                encode_room_type(request.form['room_type']),
                float(request.form['lead_time']),
                encode_market_segment(request.form['market_segment_type']),
                float(request.form['repeated']),
                float(request.form['p_c']),
                float(request.form['p_not_c']),
                float(request.form['average_price']),
                float(request.form['special_requests']),
                encode_reservation_date(request.form['date_of_reservation'])
            ]

            input_scaled = scaler.transform([input_data])

            result = model.predict(input_scaled)[0]
            prediction = "Not Canceled" if result == 0 else "Canceled"

        except Exception as e:
            prediction = f"Error: {e}"

    return render_template('index.html', prediction=prediction)

# -----------------------------
# Encoding functions based on value counts you provided

def encode_meal(meal_type):
    meal_map = {
        'Meal Plan 1': 0,
        'Not Selected': 1,
        'Meal Plan 2': 2,
        'Meal Plan 3': 3
    }
    return meal_map.get(meal_type, -1)

def encode_room_type(room_type):
    room_map = {
        'Room_Type 1': 0,
        'Room_Type 4': 1,
        'Room_Type 6': 2,
        'Room_Type 2': 3,
        'Room_Type 5': 4,
        'Room_Type 7': 5,
        'Room_Type 3': 6
    }
    return room_map.get(room_type, -1)

def encode_market_segment(segment_type):
    segment_map = {
        'Online': 0,
        'Offline': 1,
        'Corporate': 2,
        'Complementary': 3,
        'Aviation': 4
    }
    return segment_map.get(segment_type, -1)

def encode_reservation_date(date_string):
    try:
        # Assuming input is 'YYYY-MM-DD' from HTML form
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        # Example encoding: day of year
        return date_obj.timetuple().tm_yday
    except:
        return -1

# -----------------------------

if __name__ == '__main__':
    app.run(debug=True)
