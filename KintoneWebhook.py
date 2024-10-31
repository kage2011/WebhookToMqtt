from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    print("Webhook received!")
    data = request.json
    print("Received data:", data)  # 受信データをログに記録
    return "Webhook received", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
