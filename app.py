from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
BREVO_SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL")
BREVO_RECEIVE_EMAIL = os.getenv("BREVO_RECEIVE_EMAIL")

@app.route('/webhook', methods=['POST'])
def rfq_webhook():
    try:
        data = request.get_json()
        subject = "【新RFQ询盘通知】收到海外客户需求"
        html_content = f"<pre>{data}</pre>"

        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "api-key": BREVO_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "sender": {"email": BREVO_SENDER_EMAIL},
            "to": [{"email": BREVO_RECEIVE_EMAIL}],
            "subject": subject,
            "htmlContent": html_content
        }
        requests.post(url, headers=headers, json=payload)
        return jsonify({"status":"ok","msg":"RFQ已接收，邮件推送成功"}),200
    except Exception as e:
        return jsonify({"status":"fail","error":str(e)}),500

@app.route('/', methods=['GET'])
def index():
    return "RFQ Webhook Service Running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
