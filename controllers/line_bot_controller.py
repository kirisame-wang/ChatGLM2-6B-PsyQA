'''
當用戶關注時，必須取用照片，並存放至指定bucket位置，而後生成User物件，存回db
當用戶取消關注時，
    從資料庫提取用戶數據，修改用戶的封鎖狀態後，存回資料庫
'''

from services import UserService, TextService
from utils import line_bot_api, set_rich_menu


class LineBotController:
    # 獲取現有的 Rich Menu 列表
    rich_menu_list = line_bot_api.get_rich_menu_list()
    if not rich_menu_list:
        set_rich_menu()

    # 將消息交給用戶服務處理
    @classmethod
    def follow_event(cls, event):
        UserService.line_user_follow(event)
        return "OK"

    @classmethod
    def unfollow_event(cls, event):
        UserService.line_user_unfollow(event)
        return "OK"

    # TODO: 未來可能會判斷用戶快取狀態，現在暫時無
    @classmethod
    def handle_text_message(cls, event):
        TextService.line_user_reply_text(event)
        return "OK"

    @classmethod
    def handle_image_message(cls, event):
        # ImageService.line_user_upload_image(event)
        # return "OK"
        pass

    @classmethod
    def handle_video_message(cls, event):
        # VideoService.line_user_upload_video(event)
        # return "OK"
        pass

    @classmethod
    def handle_audio_message(cls, event):
        # AudioService.line_user_upload_audio(event)
        # return "OK"
        pass

    # 擷取event的data欄位，並依照function_name，丟入不同的方法
    @classmethod
    def handle_postback_event(cls, event):
        # query string 拆解 event.postback.data
        # query_string_dict = parse_qs(event.postback.data)

        # 擷取功能
        # detect_function_name = query_string_dict.get('function_name')[0]

        # Postbakc function 功能對應轉發

        # return 'no'
        pass
