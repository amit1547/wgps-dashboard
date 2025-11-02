import os
import json
import threading
import time
import paho.mqtt.client as mqtt

# ✅ Dynamic path for Render or local
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "mqtt_device_log.txt")

# ✅ Thread-safe log writing
log_lock = threading.Lock()

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        line = json.dumps(data)
        with log_lock:
            with open(LOG_FILE, "a") as f:
                f.write(line + "\n")
        print("Logged:", data.get("devid", "unknown"))
    except Exception as e:
        print("Error parsing MQTT message:", e)

def start_mqtt():
    def on_connect(client, userdata, flags, rc):
        print("MQTT connected with result code", rc)
        client.subscribe("irwgps/WAPL/data/json")

    client = mqtt.Client()
    client.username_pw_set("tnt", "syook2018")
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect("test-2-mqtt.syookinsite.com", 1883, 60)
        client.loop_start()
        print("MQTT loop started")
    except Exception as e:
        print("MQTT connection failed:", e)

# ✅ Parse latest data per device
def get_latest_data():
    if not os.path.exists(LOG_FILE):
        print("Log file not found")
        return []
    latest = {}
    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                devid = data.get("devid")
                if devid:
                    latest[devid] = data
            except:
                continue
    return list(latest.values())

# ✅ Parse full history for a device
def get_device_history(devid):
    if not os.path.exists(LOG_FILE):
        print("Log file not found")
        return []
    history = []
    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                if data.get("devid") == devid:
                    history.append(data)
            except:
                continue
    return history
