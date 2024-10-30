import paho.mqtt.client as mqtt
import json
from flask import Flask, request

app = Flask(__name__)

# MQTT設定
mqtt_broker = "broker.hivemq.com"
mqtt_port = 8884
mqtt_topic = "kintone/button"

# MQTTクライアントの設定
client = mqtt.Client(transport="websockets")
client.tls_set()
client.connect(mqtt_broker, mqtt_port, 60)

print("test")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    payload = json.dumps(data)
    client.publish(mqtt_topic, payload)
    return "Webhook received and MQTT message sent", 200

if __name__ == '__main__':
    app.run(port=5000)

