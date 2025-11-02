from flask import Flask, render_template, jsonify
from mqtt_handler import start_mqtt, get_latest_data, get_device_history

app = Flask(__name__)
start_mqtt()  # ← this runs even under gunicorn
app.run(debug=True)

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/devices')
def devices():
    return jsonify(get_latest_data())

@app.route('/history/<devid>')
def history(devid):
    return jsonify(get_device_history(devid))
