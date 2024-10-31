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

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

client.on_connect = on_connect

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    payload = json.dumps(data)
    
    # Webhookを受け取った際にMQTTブローカーに接続
    client.connect(mqtt_broker, mqtt_port, 60)
    # client.loop_start()  # ループをバックグラウンドで開始
    
    try:
        result = client.publish(mqtt_topic, payload)
        result.wait_for_publish()
        print("MQTT message sent!")
    except Exception as e:
        print("Failed to send MQTT message:", e)
    
    # client.loop_stop()  # ループを停止
    client.disconnect()  # 接続を切断
    
    return "Webhook received and MQTT message sent", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
