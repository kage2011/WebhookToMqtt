import os
import paho.mqtt.client as mqtt
import json
from flask import Flask, request

app = Flask(__name__)

# 環境変数からMQTT設定を取得
mqtt_broker = os.getenv("MQTT_BROKER", "broker.hivemq.com")
mqtt_port = int(os.getenv("MQTT_PORT", 8884))
mqtt_topic = os.getenv("MQTT_TOPIC", "kintone/comment/webhook")

# # MQTTブローカーの設定
# mqtt_broker = "broker.hivemq.com"
# mqtt_port = 8884
# mqtt_topic = "kintone/comment/webhook"

# MQTTクライアントの設定
client = mqtt.Client(transport="websockets")
client.tls_set()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

def on_publish(client, userdata, mid):
    print("Message Published!")

client.on_connect = on_connect
client.on_publish = on_publish
client.connect(mqtt_broker, mqtt_port, 60)
# client.loop_start()

@app.route('/webhook', methods=['POST'])
def webhook():
    print("hooking!")
    data = request.json
    print("Received webhook data:", data)  # 受信データをログに記録
    payload = json.dumps(data)
    try:
        result = client.publish(mqtt_topic, payload)
        result.wait_for_publish()
        print("MQTT message sent!")
    except Exception as e:
        print("Failed to send MQTT message:", e)
    return "Webhook received and MQTT message sent", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
