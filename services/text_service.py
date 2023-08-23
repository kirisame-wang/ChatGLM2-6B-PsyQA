import json
import random
import requests

from bs4 import BeautifulSoup
from googletrans import Translator
from linebot.models import *
from opencc import OpenCC
from peft import PeftModel
from transformers import AutoTokenizer, AutoModel, pipeline

from daos import UserDAO
from utils import line_bot_api


tokenizer = AutoTokenizer.from_pretrained("checkpoints/chatglm2", trust_remote_code=True)
base_model = AutoModel.from_pretrained("checkpoints/chatglm2", trust_remote_code=True, device='cuda')
model = PeftModel.from_pretrained(base_model, "checkpoints/qlora-v5")
classifier = pipeline("sentiment-analysis", model="checkpoints/distilbert", device='cuda')

print("Model is loaded.")
print("Start chatbot.")


class TextService:
    @classmethod
    def line_user_reply_text(cls, event):
        cls.user = UserDAO.get_user(event.source.user_id)
        # cls.line_bot_state = cls.user.line_bot_state
        if not cls.user:
            line_bot_api.reply_message(
                event.reply_token,
                messages=[TextSendMessage("沒有用戶資料，請封鎖並解除封鎖機器人後重新再試。")])
            return
        if event.message.text == '近期的心理文章':
            cls.get_psy_info(event)
        elif event.message.text == "清空對話紀錄":
            cls.user.line_bot_history = json.dumps([], ensure_ascii=False)
            UserDAO.save_user(cls.user)
            line_bot_api.reply_message(
                event.reply_token,
                messages=[TextSendMessage("好的，已清空對話紀錄。")])
        else:
            cls.chat_with_llm(event)

    @classmethod
    def chat_with_llm(cls, event):
        # ChatGLM2-6B-PsyQA
        cc = OpenCC('tw2s')
        input_text = cc.convert(event.message.text)

        prmpts = ""
        if len(input_text.split()) >= 10 or len(input_text) >= 10:
            prmpts = "请假装你是一个心理咨询师，根据下列发问者所提供之问题给出意识流，并以第一人称口吻答复。\n问题描述："
        print(f"输入：\n{prmpts + input_text}\n")
        response, history = model.chat(tokenizer, prmpts + input_text,
                                       history=json.loads(cls.user.line_bot_history),
                                       repetition_penalty=1.2)
        history = [(_[0].lstrip(prmpts), _[1]) for _ in history[-10:]]
        cls.user.line_bot_history = json.dumps(history, ensure_ascii=False)

        cc = OpenCC('s2tw')
        response = '\n'.join(response.replace(". ", ".").split()).replace(",", "，").replace(".", ". ")
        response = cc.convert(response)
        print(f"回复：{response}")
        messages = [TextSendMessage(response)]

        # DistilBert
        if len(input_text.split()) >= 4 or len(input_text) >= 4:
            translator = Translator()
            input_text = translator.translate(input_text, dest='en').text
            bert_result = classifier(input_text)[0]
            print(f"風險評分：{bert_result}")

            if bert_result["label"] == "LABEL_1" and bert_result['score'] > 0.85:
                cls.user.user_risk_score = round(bert_result['score'] * 100)
                messages.append(TextSendMessage("\n".join([
                    "自殺不能解決問題，勇敢求救並非弱者，生命一定可以找到出路。",
                    "透過守門123步驟-1問2應3轉介，你我都可以成為自殺防治守門人。",
                    "※安心專線：1925",
                    "※張老師專線：1980",
                    "※生命線專線：1995"
                ])))

        line_bot_api.reply_message(event.reply_token, messages=messages)
        UserDAO.save_user(cls.user)

    @classmethod
    def get_psy_info(cls, event):
        # 要爬取的網頁 URL
        url = "https://www.iiispace.com/blog/"

        # 發送 HTTP GET 請求並獲取網頁內容
        response = requests.get(url)
        html_content = response.text

        # 使用 BeautifulSoup 解析 HTML 內容
        soup = BeautifulSoup(html_content, "html.parser")

        # 找到所有文章標題和連結
        data = []
        articles = soup.find_all("h2")
        # 爬取20篇文章資訊
        for article in articles[:20]:
            title = article.a.text
            link = article.a["href"]
            article_response = requests.get(link)
            article_html = article_response.text
            article_soup = BeautifulSoup(article_html, "html.parser")
            image = article_soup.find("img", class_="enigma_img_responsive wp-post-image")
            image_url = image["src"] if image else "沒有圖片"
            data.append((title, link, image_url))

        carousel_columns = []
        random_sample = random.sample(data, 5)
        for title, link, image_url in random_sample:
            carousel_column = CarouselColumn(
                thumbnail_image_url=image_url,
                title="近期的心理文章",
                text=title,
                actions=[
                    URIAction(label="詳細內容", uri=link)
                ]
            )
            carousel_columns.append(carousel_column)

        carousel_template = CarouselTemplate(columns=carousel_columns)

        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text="心理相關資訊", template=carousel_template)
        )
