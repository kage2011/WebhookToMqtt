import os
import paho.mqtt.client as mqtt
import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    print("hooking!")
    data = request.json
    print("Received webhook data:", data)  # 受信データをログに記録
    payload = json.dumps(data)
    print(payload)
    return "Webhook received and MQTT message sent", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
