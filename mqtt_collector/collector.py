import paho.mqtt.client as mqtt_client
import time
import datetime
import os
import json
import requests
import logging

logger = logging.getLogger(__name__)

# Define the MQTT settings
broker_address = "node02.myqtthub.com"  # Replace with your MQTT broker address
broker_port = 1883                  # Default MQTT port
topic = "sensor/temperature"        # Topic to publish to
client_id = "ArduinoRev4WiFi"         # Unique client ID
username = os.environ["USER"]        # Replace with your broker username (if required)
password = os.environ["PASSWORD"]          # Replace with your broker password (if required)

py_server_endpoint = os.environ["PY_SERVER_ENDPOINT"]

def wait_for_server_to_respond():
    ready = False
    for i in range(10):
        try:
            requests.get(py_server_endpoint)
        except Exception:
            print("Waiting for endpoint...")
            time.sleep(1)
            pass

        ready = True

    return ready

# Callback function when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected")
        client.subscribe(topic)
    else:
        print("Connection failed with code", rc)

# Callback function when a message is received on the subscribed topic
def on_message(client, userdata, msg):
    print("Message")
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    msg_topic = msg.topic
    msg_timestamp = str(datetime.datetime.now())

    if msg_topic == topic:

        print(f"Received message on topic: {msg_topic} at {msg_timestamp}")
        # Here you can process the message further if needed
        # For example, if you're expecting a number (e.g., temperature):
        try:
            data = json.loads(msg.payload.decode())
            temperature = float(data["temp"])
            logger.error(f"Temperature value: {temperature}°C")

            requests.post(py_server_endpoint, json={"temp": temperature})

        except ValueError:
            logger.error(f"Received non-numeric data: {msg.payload.decode()}")


def on_disconnect(client, userdata, rc):
    print("Disconnected from broker")

# Create a new MQTT client instance
client = mqtt_client.Client(client_id)

# Set username and password for the client (if required)
client.username_pw_set(username, password)

client.subscribe(topic, qos=1)

# Assign the callback functions
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# Try connecting to the broker
try:

    ready = wait_for_server_to_respond()

    if not ready:
        raise Exception("Endpoint not reached")

    print(f"Attempting to connect to broker: {broker_address}")
    client.connect(broker_address, broker_port, 60)  # Timeout is set to 60 seconds

    client.loop_start()  # Start the MQTT client loop in non-blocking mode

    # Keep the script running while waiting for messages
    print(f"Subscribed to {topic} and waiting for messages...")

    while True:
        time.sleep(0.5)  # Small delay to avoid high CPU usage while listening

except Exception as e:
    print(f"Error occurred: {str(e)}")