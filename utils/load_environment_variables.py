import configparser

from linebot import LineBotApi, WebhookHandler


config = configparser.ConfigParser()
config.read("config.ini")

handler = WebhookHandler(channel_secret=config["DEFAULT"]["LINE_CHANNEL_SECRET"])
line_bot_api = LineBotApi(channel_access_token=config["DEFAULT"]["LINE_CHANNEL_ACCESS_TOKEN"])
ngrok_auth_token = config["DEFAULT"]["NGROK_AUTH_TOKEN"]