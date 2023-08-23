'''
line用戶關注時，儲存line用戶個資時，取照片，更換連結，放回原object，
line用戶封鎖時，將資料庫內的用戶資料更改為已封鎖。
取出用戶個資時，傳入用戶id，作為檢索條件
'''

import urllib.request

from linebot.models import TextSendMessage

from daos import UserDAO
from models import User
from utils import line_bot_api


class UserService:
    '''
    取得line event，將line event拿去取個資，轉換成User，並將其照片取出，存回cloud storage，
    並用cloudstorage的連結取代user的line圖片連結
    '''

    @classmethod
    def line_user_follow(cls, event) -> None:
        # Welcome message
        line_bot_api.reply_message(
            event.reply_token,
            messages=[TextSendMessage("哈囉，歡迎來到心理聊天室，有什麼問題都可以跟我說呦！")])

        # Parse the user's profile
        line_user_profile = line_bot_api.get_profile(event.source.user_id)
        user = User(
            line_user_id=line_user_profile.user_id,
            line_user_pic_url=line_user_profile.picture_url,
            line_user_nickname=line_user_profile.display_name,
            line_user_status=line_user_profile.status_message,
            line_user_system_language=line_user_profile.language
            )

        '''
        先確認用戶的照片連結是否正常，
            若存在，取得用戶照片，存放回cloud storage
            並將連結存回user的連結
        '''
        if user.line_user_pic_url is not None:
            # 跟line 取回照片，並放置在本地端
            file_name = f"users/pics/{user.line_user_id}.jpg"
            urllib.request.urlretrieve(user.line_user_pic_url, file_name)

            # 上傳至bucket
            # storage_client = storage.Client()
            # destination_blob_name = f'{user.line_user_id}/user_pic.png'
            # bucket = storage_client.bucket(bucket_name)
            # blob = bucket.blob(destination_blob_name)
            # blob.upload_from_filename(file_name)

            # 更新回user的圖片連結
            # destination_url = f'https://storage.googleapis.com/{bucket_name}/{user.line_user_id}/user_pic.png'
            user.line_user_pic_url = file_name

        # 存入資料庫
        UserDAO.save_user(user)

        # 移除本地檔案
        # os.remove(file_name)

        # 打印結果
        # print(user)

        # 回傳結果給handler
        # 關注的部分，不回傳，交由控制台回傳
        pass


    @classmethod
    def line_user_unfollow(cls, event) -> None:
        # Get the user's profile and update the blocked state
        user = UserDAO.get_user(event.source.user_id)
        user.blocked = True
        UserDAO.save_user(user)
        # print(user)
        # print('用戶已封鎖')


    @classmethod
    def get_user(cls, user_id: str) -> User:
        # Get the user's data in the database with the user's id
        user = UserDAO.get_user(user_id)
        # print(user)
        return user