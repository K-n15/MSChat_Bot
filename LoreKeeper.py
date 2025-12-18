import  os, json, logging, hashlib, sys, requests
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
    if body["object"] == "page":
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", file=sys.stdout)
        print("I RECEIVED A MESSAGE!", file=sys.stdout)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", file=sys.stdout)
        logger.info('start page logging')
        logger.info(body["entry"])
        logger.info('end page logging')
        return "EVENT_RECEIVED",200
    return "PAGE_NOT_FOUND",404

def send_message(recipient_id, message_text):

    logger.info("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        err = str(r.status_code) + " " + r.text
        logger.info(err)