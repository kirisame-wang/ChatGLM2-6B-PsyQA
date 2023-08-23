'''

用戶上傳照片時，將照片從Line取回，放入CloudStorage

瀏覽用戶目前擁有多少張照片（未）

'''
from linebot.models import TextSendMessage

from utils import line_bot_api


class ImageService:
    @classmethod
    def line_user_upload_image(cls, event):
        line_bot_api.reply_message(
            event.reply_token,
            messages=TextSendMessage("已收到您的資料。"))
