import logging
import os
import sys

from flask import Flask, request, abort
from linebot.exceptions import InvalidSignatureError
from linebot.models.events import FollowEvent, UnfollowEvent, MessageEvent, TextMessage, PostbackEvent, ImageMessage, \
    AudioMessage, VideoMessage
from pyngrok import ngrok

from controllers import LineBotController
from utils import handler, ngrok_auth_token


# Append the root path
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]

sys.path.append(rootPath)


# Initiate google logging (https://googleapis.dev/python/logging/latest/stdlib-usage.html)
# client = google.cloud.logging.Client()

# Initiate line event log
# bot_event_handler = CloudLoggingHandler(client, name="ncu_bot_event")
# bot_event_logger = logging.getLogger('ncu_bot_event')
# bot_event_logger.setLevel(logging.INFO)
# bot_event_logger.addHandler(bot_event_handler)

# Initiate the app
app = Flask(__name__)
# CORS(app)


@app.route('/test')
def hello_world():
    # bot_event_logger.info("test")
    return 'Hello, World!'


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    # bot_event_logger.info(body)
    # print(body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


@app.route("/user", methods=['GET'])
def get_user():
    # result = UserController.get_user(request)
    # return result
    pass


@handler.add(FollowEvent)
def handle_line_follow(event):
    return LineBotController.follow_event(event)


@handler.add(UnfollowEvent)
def handle_line_unfollow(event):
    return LineBotController.unfollow_event(event)


@handler.add(MessageEvent, message=TextMessage)
def handle_line_text(event):
    return LineBotController.handle_text_message(event)


@handler.add(MessageEvent, message=ImageMessage)
def handle_line_image(event):
    # return LineBotController.handle_image_message(event)
    pass


@handler.add(MessageEvent, message=VideoMessage)
def handle_line_video(event):
    # return LineBotController.handle_video_message(event)
    pass


@handler.add(MessageEvent, message=AudioMessage)
def handle_line_audio(event):
    # return LineBotController.handle_audio_message(event)
    pass


@handler.add(PostbackEvent)
def handle_postback_event(event):
    # return LineBotController.handle_postback_event(event)
    pass


if __name__ == "__main__":
    ngrok.set_auth_token(ngrok_auth_token)
    print(ngrok.connect(5000).public_url)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
