from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Doctors data
doctors = [
    {
        "id": 1,
        "name": "Dr. John Doe",
        "location": "Hospital A",
        "evenings": [
            {"day": "Monday", "start_time": "18:00", "end_time": "20:00"},
            {"day": "Wednesday", "start_time": "18:00", "end_time": "20:00"},
        ],
        "max_patients": 10,
    },
    {
        "id": 2,
        "name": "Dr. Jane Smith",
        "location": "Hospital B",
        "evenings": [
            {"day": "Tuesday", "start_time": "18:00", "end_time": "20:00"},
            {"day": "Thursday", "start_time": "18:00", "end_time": "20:00"},
        ],
        "max_patients": 15,
    },
]

appointments = []


@app.route("/doctors", methods=["GET"])
def get_doctors():
    return jsonify(doctors)


@app.route("/doctors/<int:doctor_id>", methods=["GET"])
def get_doctor(doctor_id):
    doctor = next((doc for doc in doctors if doc["id"] == doctor_id), None)
    if doctor:
        return jsonify(doctor)
    else:
        return jsonify({"error": "Doctor not found"}), 404


@app.route("/appointments", methods=["POST"])
def book_appointment():
    data = request.get_json()
    doctor_id = data["doctor_id"]
    appointment_date = data["appointment_date"]
    appointment_time = data["appointment_time"]

    doctor = next((doc for doc in doctors if doc["id"] == doctor_id), None)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    # Check if appointment date is a valid weekday evening
    weekday = datetime.strptime(appointment_date, "%Y-%m-%d").weekday()
    if weekday % 2 == 0 or appointment_time < doctor["evenings"][0]["start_time"] or appointment_time > doctor["evenings"][0]["end_time"]:
        return jsonify({"error": "Invalid appointment date or time"}), 400

    # Check if doctor is already fully booked for the day
    if len(appointments) >= doctor["max_patients"]:
        return jsonify({"error": "Doctor is fully booked"}), 400

    # Check for conflicting appointments
    for appt in appointments:
        if appt["doctor_id"] == doctor_id and appt["appointment_date"] == appointment_date and appt["appointment_time"] == appointment_time:
            return jsonify({"error": "Appointment already booked"}), 400

    # Create new appointment
    new_appointment = {
        "id": len(appointments) + 1,
        "doctor_id": doctor_id,
        "appointment_date": appointment_date,
        "appointment_time": appointment_time,
    }
    appointments.append(new_appointment)

    return jsonify(new_appointment), 201


if __name__ == "__main__":
    app.run(debug=True)
