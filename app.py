from flask import Flask, request
import requests, os

app = Flask(__name__)
VERIFY_TOKEN = "cuetxbot123"

@app.route("/")
def home():
    return "CUET X BOT Live - Working!"

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        value = data['entry'][0]['changes'][0]['value']
        if 'messages' in value:
            msg = value['messages'][0]
            from_num = msg['from']
            text = msg['text']['body'].lower()
            
            if "syllabus" in text:
                reply = "📚 CUET 2026 Syllabus: https://cuetx.com/syllabus"
            elif "pyq" in text or "previous" in text:
                reply = "📄 PYQ yahan milega: https://cuetx.com/pyq"
            elif "mock" in text:
                reply = "🧪 Mock Test: https://cuetx.com/mock"
            else:
                reply = f"Namaste! Main CUET X BOT hu. Tumne bola: {text}. Syllabus, PYQ, Mock me se ek likho."

            url = f"https://graph.facebook.com/v20.0/1402750426255148/messages"
            headers = {
                "Authorization": f"Bearer {os.environ.get('ACCESS_TOKEN')}",
                "Content-Type": "application/json"
            }
            payload = {
                "messaging_product": "whatsapp",
                "to": from_num,
                "type": "text",
                "text": {"body": reply}
            }
            requests.post(url, headers=headers, json=payload)
    except Exception as e:
        print(e)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
