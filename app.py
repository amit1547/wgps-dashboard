from flask import Flask, render_template, jsonify
from mqtt_handler import start_mqtt, get_latest_data, get_device_history

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/devices')
def devices():
    return jsonify(get_latest_data())

@app.route('/history/<devid>')
def history(devid):
    return jsonify(get_device_history(devid))

if __name__ == '__main__':
    start_mqtt()
    app.run(debug=True)
