
python 
from flask import Flask, jsonify, request
from datetime import datetime, timedelta

app = Flask(__name__)

# Sample data
doctors = [
    {
        "id": 1,
        "name": "Dr. John Doe",
        "location": "Hospital A",
        "evenings": [
            {"day": "Monday", "start_time": "18:00", "end_time": "20:00"},
            {"day": "Wednesday", "start_time": "18:00", "end_time": "20:00"},
        ],
        "patient_limit": 10,
    },
    {
        "id": 2,
        "name": "Dr. Jane Smith",
        "location": "Hospital B",
        "evenings": [
            {"day": "Tuesday", "start_time": "18:00", "end_time": "20:00"},
            {"day": "Thursday", "start_time": "18:00", "end_time": "20:00"},
        ],
        "patient_limit": 15,
    },
]

appointments = []

@app.route("/doctors", methods=["GET"])
def get_doctors():
    return jsonify({"doctors": doctors})

@app.route("/doctors/<int:doctor_id>", methods=["GET"])
def get_doctor_detail(doctor_id):
    doctor = next((doc for doc in doctors if doc["id"] == doctor_id), None)
    if doctor:
        return jsonify({"doctor": doctor})
    else:
        return jsonify({"error": "Doctor not found"}), 404

@app.route("/doctors/<int:doctor_id>/appointments", methods=["POST"])
def book_appointment(doctor_id):
    if not request.is_json:
        return jsonify({"error": "Invalid request format"}), 400

    data = request.get_json()
    patient_name = data.get("patient_name", None)
    appointment_date = data.get("appointment_date", None)

    if not patient_name or not appointment_date:
        return jsonify({"error": "Missing required fields"}), 400

    doctor = next((doc for doc in doctors if doc["id"] == doctor_id), None)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d")
    day = appointment_date.strftime("%A")
    start_time = datetime.strptime(data.get("start_time", ""), "%H:%M")
    end_time = datetime.strptime(data.get("end_time", ""), "%H:%M")

    if not start_time or not end_time:
        return jsonify({"error": "Invalid start or end time"}), 400

    if appointment_date.weekday() % 2 == 0:
        return jsonify({"error": "Appointments can only be booked on evenings"}), 400

    if len(appointments) >= doctor["patient_limit"]:
        return jsonify({"error": "Doctor's patient limit reached"}), 400

    for appt in appointments:
        if appt["doctor_id"] == doctor_id and appt["appointment_date"].date() == appointment_date.date():
            return jsonify({"error": "Appointment already booked for this date"}), 400

    appointment = {
        "id": len(appointments) + 1,
        "doctor_id": doctor_id,
        "patient_name": patient_name,
        "appointment_date": appointment_date,
        "start_time": start_time,
        "end_time": end_time,
    }
    appointments.append(appointment)

    return jsonify({"appointment": appointment}), 201

if __name__ == "__main__":
    app.run(debug=True)
