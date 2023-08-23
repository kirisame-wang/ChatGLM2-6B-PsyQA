'''

用戶上傳照片時，將照片從Line取回，放入CloudStorage

瀏覽用戶目前擁有多少張照片（未）

'''

import os

from linebot.models import TextSendMessage

from utils import line_bot_api


class VideoService:
    '''
    用戶上傳影片
    將照片取回
    將照片存入CloudStorage內
    '''

    @classmethod
    def line_user_upload_video(cls, event):
        # 取出影片
        image_blob = line_bot_api.get_message_content(event.message.id)
        temp_file_path = f"""{event.message.id}.mp4"""

        #
        with open(temp_file_path, 'wb') as fd:
            for chunk in image_blob.iter_content():
                fd.write(chunk)

        # 上傳至bucket
        # storage_client = storage.Client()
        # destination_blob_name = f'{event.source.user_id}/video/{event.message.id}.mp4'
        # bucket = storage_client.bucket(bucket_name)
        # blob = bucket.blob(destination_blob_name)
        # blob.upload_from_filename(temp_file_path)

        # 移除本地檔案
        # os.remove(temp_file_path)

        # 回覆消息
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("影片已上傳，請期待未來的AI服務！")
        )
