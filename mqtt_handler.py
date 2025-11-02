import paho.mqtt.client as mqtt
import json
import os

LOG_FILE = "mqtt_device_log.txt"
device_data = {}

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        if all(k in payload for k in ["devid", "dtpt", "lat", "lng"]):
            devid = payload["devid"]
            device_data[devid] = payload
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(payload) + "\n")
    except Exception as e:
        print("Error:", e)

def start_mqtt():
    client = mqtt.Client()
    client.username_pw_set("tnt", "syook2018")
    client.on_message = on_message
    client.connect("test-2-mqtt.syookinsite.com", 1883, 60)
    client.subscribe("irwgps/WAPL/data/json")
    client.loop_start()

def get_latest_data():
    return list(device_data.values())

def get_device_history(devid):
    history = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    payload = json.loads(line)
                    if payload.get("devid") == devid:
                        history.append(payload)
                except:
                    continue
    return history
