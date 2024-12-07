from flask import Flask, request, jsonify, render_template
import sqlite3
import uuid

class Booking:
    def __init__(self, date, car_category, hours, fare):
        self.id = uuid.uuid4().hex
        self.date = date
        self.car_category = car_category
        self.hours = hours
        self.fare = fare

app = Flask(__name__)

#Initialize database
def connect_db():
    conn = sqlite3.connect("car_rental.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS BOOKINGS(
            id TEXT, 
            date TEXT, 
            car_category TEXT, 
            hours INTEGER, 
            fare REAL
        )
    """)
    conn.commit()
    conn.close()

# Fare Calculation
def calculate_fare(car_category, hours):
    rates = {
        "classic": 100,  # 100 BDT/hour
        "premium": 200,  # 200 BDT/hour
        "microbus": 300,  # 300 BDT/hour
    }
    return rates[car_category] * hours

@app.route('/')
def index():
    connect_db() 
    return render_template('test.html')

@app.route('/getCars', methods=['GET'])
def getCars():
    cars = [
        {"category": "classic", "description": "Affordable, up to 4 passengers", "rate_per_hour": 100},
        {"category": "premium", "description": "Comfortable, up to 6 passengers", "rate_per_hour": 200},
        {"category": "microbus", "description": "Spacious, up to 14 passengers", "rate_per_hour": 300}
    ]
    return jsonify(cars)

@app.route('/addBooking', methods=['POST'])
def addBooking():
    db = sqlite3.connect('car_rental.db')
    c = db.cursor()
    
    data = request.form
    date = data['date']
    car_category = data['car_category']
    hours = int(data['hours'])
    fare = calculate_fare(car_category, hours)
    
    booking = Booking(date, car_category, hours, fare)
    c.execute("INSERT INTO BOOKINGS VALUES(?, ?, ?, ?, ?)", 
              (booking.id, booking.date, booking.car_category, booking.hours, booking.fare))
    db.commit()
    db.close()
    
    return render_template('confirmation.html', booking_id=booking.id, fare=fare)

@app.route('/viewBookings', methods=['GET'])
def viewBookings():
    db = sqlite3.connect('car_rental.db')
    c = db.cursor()
    c.execute("SELECT * FROM BOOKINGS")
    data = c.fetchall()
    db.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=1087)