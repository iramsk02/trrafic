from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, jsonify
import os
import threading
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Create a directory for storing uploaded videos
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Sample data for analytics and map points
analytics_data = {
    "Total Videos": 10,
    "Total Analyzed": 8,
    "Average Processing Time": "3 minutes",
}

map_data = [
    {"location": "Signal 1", "lat": 37.7749, "lng": -122.4194, "status": "Heavy Traffic"},
    {"location": "Signal 2", "lat": 34.0522, "lng": -118.2437, "status": "Moderate Traffic"},
    {"location": "Signal 3", "lat": 40.7128, "lng": -74.0060, "status": "Smooth Traffic"},
]

# Dictionary to hold the detected vehicle data
detected_vehicles_data = []

# Placeholder function to simulate vehicle detection
def simulate_vehicle_detection():
    global detected_vehicles_data
    while True:
        detected_vehicles_data = [
            {"signal": "Signal 1", "vehicles_detected": 12},
            {"signal": "Signal 2", "vehicles_detected": 7},
            {"signal": "Signal 3", "vehicles_detected": 15},
        ]
        print("Simulating vehicle detection...")
        time.sleep(120)  # 2 minutes interval

# Start the background thread for vehicle detection simulation
detection_thread = threading.Thread(target=simulate_vehicle_detection)
detection_thread.daemon = True
detection_thread.start()

# Route for the home page (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route for uploading videos
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'video' not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files['video']
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            flash("File uploaded successfully!")
            return redirect(url_for('uploaded_videos'))
    return render_template('upload.html')  # Create this page if needed

# Route for displaying uploaded videos with delete functionality
@app.route('/uploads')
def uploaded_videos():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('uploads.html', files=files)

# Route for serving uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Route for deleting a video file
@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f"{filename} has been deleted.")
    else:
        flash(f"{filename} not found.")
    return redirect(url_for('uploaded_videos'))

# Route for traffic analysis dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    signals = ["Signal 1", "Signal 2", "Signal 3"]
    analysis_result = None
    selected_signal = None

    if request.method == 'POST':
        selected_signal = request.form['signal']
        analysis_result = f"Analysis for {selected_signal}: Traffic flow is smooth."

    return render_template('dashboard.html', signals=signals, selected_signal=selected_signal, analysis=analysis_result)

# Route for analytics dashboard
@app.route('/analytics')
def analytics():
    return render_template('analytics.html', analytics=analytics_data)

# Route for map view
@app.route('/map')
def map_view():
    return render_template('map.html', map_points=map_data)

# Route for live vehicle detection data
@app.route('/vehicle_detection')
def vehicle_detection():
    return render_template('vehicle_detection.html', detected_vehicles=detected_vehicles_data)

# Route for fetching live vehicle detection data as JSON
@app.route('/api/vehicle_detection', methods=['GET'])
def api_vehicle_detection():
    return jsonify(detected_vehicles_data)

if __name__ == '__main__':
    app.run(debug=True)
