import  os, datetime, json, logging, hashlib, sys
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

@app.route("/webhook",methods=['POST'])
def ReceiveWebhook():
    body = request.json
    if body["object"] == "page":
        logger.info('start page logging')
        logger.info(body["entry"])
        logger.info('end page logging')
        return "EVENT_RECEIVED",200
    return "PAGE_NOT_FOUND",404

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
    
@app.route("/wakeup",method=['GET'])
def WakeupCall():
    logger.info("Wakeup call at")