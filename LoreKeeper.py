import  os, logging, sys, requests
from Seabed import Lobster
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout  # <--- This sends it to the Render Dashboard
)
# Use for debug
# logging.basicConfig(filename='myapp.log', level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/webhook",methods=['GET'])
def Verify():
    logger.info("REQUEST_VERIFY_ACCEPTED")
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if (mode == "subscribe" and token == os.getenv("MY_TOKEN")):
        logger.info("WEBHOOK_VERIFIED")
        return challenge,200
    else:
        logger.info("WEBHOOK_DENIED")
        return "Forbidden",403
    
@app.route("/wakeup",methods=['GET'])
def WakeupCall():
    return "Wake up call, OK", 200

@app.route("/webhook",methods=['POST'])
def ReceiveWebhook():
    body = request.json
    print("\n=============== INCOMING MESSAGE ===============", flush=True)
    if body["object"] == "page":
        for entry in body["entry"]:
            for event in entry["messaging"]:
                if event.get("message"):
                    sender_id = event["sender"]["id"]
                    send_message(sender_id, "Heard that")
                elif event.get("message") == "news":
                    print("\n=============== SENDING NEWS ===============", flush=True)
                    sender_id = event["sender"]["id"]
                    latestNews,url = Scraper.getLatestNew()
                    send_message(sender_id, latestNews+'\n'+url)
                else:
                        print(f"Received non-message event: {event.keys()}", flush=True)

        print("=============== END REQUEST ===============\n", flush=True)
        return "EVENT_RECEIVED", 200
    else:
        return "Not a Page Event", 404

def send_message(recipient_id, message_text):
    logger.info("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    }
    PAT = os.getenv("PAGE_ACCESS_TOKEN")
    url = f"https://graph.facebook.com/v24.0/me/messages?access_token={PAT}"
    r = requests.post(url, headers=headers, json=payload)
    if r.status_code != 200:
        err = str(r.status_code) + " " + r.text
        logger.info(err)

if __name__ == "__main__":
    Scraper = Lobster()
    app.run(port=10000)