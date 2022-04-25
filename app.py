from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, PostbackEvent, TextMessage, TextSendMessage, FlexSendMessage, ImageSendMessage
)
import json
from flex import flex
import requests
import re

app = Flask(__name__)

line_bot_api = LineBotApi('Ujy1C53Qhz0yLgTfJbwF2bLgS/N4gqqof4anOOjvcUNGUI8WV3NiikgI/bT+3qMT8uFKKAoPHU8qte/rxiKBfEcJhY4hL/hB95JbVHNJQnuejBKCmjGB24sY6opov+DBe1cV8mGihFxa8KHiZ32qGQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('151c5e4356e55ca3be5a16f7dfadf32f')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(PostbackEvent)
def postback_message(event,destination):
    print("image request")
    line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=event.postback.data,preview_image_url=event.postback.data))

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event, destination):
    message = event.message.text
    print("search: "+message)
    FlexMessage = flex(message)
    FlexMessage = json.loads(FlexMessage)
    line_bot_api.reply_message(event.reply_token,FlexSendMessage(alt_text = "迷因搜尋結果",contents = FlexMessage))

if __name__ == "__main__":
    app.run()


