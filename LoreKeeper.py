import  os, datetime, json, logging, hashlib
from flask import Flask, request


app = Flask(__name__)
logging.basicConfig(filename='myapp.log', level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/webhook",methods=['POST'])
def ReceiveWebhook():
    body = request.json
    if body["object"] == "page":
        logger.info('start page logging')
        logger.info(body["entry"])
        logger.info('end page logging')
        return "EVENT-RECEIVED",200
    return "PAGE_NOT_FOUND",404

@app.route("/webhook",methods=['GET'])
def Verify():
    logger.info("REQUEST_VERIFY_ACCEPTED")
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if (mode == "subscribe" and token == "MY_TEMP_TOKEN"):
        logger.info("WEBHOOK-VERIFIED")
        return challenge,200
    else:
        return "Forbidden",403