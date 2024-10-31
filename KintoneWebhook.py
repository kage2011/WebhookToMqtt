import os
import paho.mqtt.client as mqtt
import json
from flask import Flask, request

app = Flask(__name__)

# 環境変数からMQTT設定を取得
mqtt_broker = os.getenv("MQTT_BROKER", "broker.hivemq.com")
mqtt_port = int(os.getenv("MQTT_PORT", 8884))
mqtt_topic = os.getenv("MQTT_TOPIC", "kintone/comment/webhook")

# MQTTクライアントの設定
client = mqtt.Client(transport="websockets")
client.tls_set()
client.connect(mqtt_broker, mqtt_port, 60)

@app.route('/webhook', methods=['POST'])
def webhook():
    print("hooking!")
    data = request.json
    payload = json.dumps(data)
    client.publish(mqtt_topic, payload)
    return "Webhook received and MQTT message sent", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

