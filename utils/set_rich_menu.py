"""
創建 Rich Menu圖文選單
"""
from io import BytesIO
from PIL import Image

from linebot.exceptions import LineBotApiError
from linebot.models import *

from utils import line_bot_api


def set_rich_menu():
    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=2500, height=843),
        selected=True,
        name="rich_menu_v1",
        chat_bar_text="查看更多資訊",
        areas=[
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
                action=URIAction(label="Button 1", uri="https://forms.gle/7jbBMRh1CaphF8hv7")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=833, y=0, width=833, height=843),
                action=MessageAction(label="Button 2", text="清空對話紀錄")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=1666, y=0, width=833, height=843),
                action=MessageAction(label="Button 3", text="近期的心理文章")
            )
        ]
    )

    # 上傳 Rich Menu
    try:
        rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
        print("Rich Menu created. ID:", rich_menu_id)
    except LineBotApiError as e:
        print("Failed to create Rich Menu:", e)

    # 上傳 Rich Menu 的圖片
    image_content = BytesIO()
    image_url = "pics/rich_memu.jpg"
    image = Image.open(image_url)
    image.save(image_content, format='JPEG')
    line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', image_content.getvalue())

    # 設定預設 Rich Menu
    line_bot_api.set_default_rich_menu(rich_menu_id)

# 刪除現有的 Rich Menu
# for rich_menu in rich_menu_list:
#     line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)
