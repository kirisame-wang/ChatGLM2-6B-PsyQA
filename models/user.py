'''
基於Line給的用戶屬性，定義用戶類別
並提供 to_dict,  from_dict方法，使能在object與dict間快速轉換
提供 __repr__ 快速打印參數
'''
from __future__ import annotations

import json


class User(object):
    def __init__(self, line_user_id, line_user_pic_url, line_user_nickname,
                 line_user_status, line_user_system_language,
                 line_bot_state=None, line_bot_history=json.dumps([], ensure_ascii=False),
                 user_risk_score=0, blocked=False) -> None:
        self.line_user_id = line_user_id
        self.line_user_pic_url = line_user_pic_url
        self.line_user_nickname = line_user_nickname
        self.line_user_status = line_user_status
        self.line_user_system_language = line_user_system_language
        self.line_bot_state = line_bot_state
        self.line_bot_history = line_bot_history
        self.user_risk_score = user_risk_score
        self.blocked = blocked


    def __repr__(self) -> str:
        return (f'''User(
            line_user_id={self.line_user_id},
            line_user_pic_url={self.line_user_pic_url},
            line_user_nickname={self.line_user_nickname},
            line_user_status={self.line_user_status},
            line_user_system_language={self.line_user_system_language},
            line_bot_state={self.line_bot_state},
            line_bot_history={self.line_bot_history},
            user_risk_score={self.user_risk_score}, 
            blocked={self.blocked}
            )''')


    # source的欄位係以 資料庫欄位做為預設命名
    @staticmethod
    def from_dict(source: dict) -> User:
        user = User(
            line_user_id=source.get("line_user_id"),
            line_user_pic_url=source.get("line_user_pic_url"),
            line_user_nickname=source.get("line_user_nickname"),
            line_user_status=source.get("line_user_status"),
            line_user_system_language=source.get("line_user_system_language"),
            line_bot_state=source.get("line_bot_state"),
            line_bot_history=source.get("line_bot_history"),
            user_risk_score=source.get("user_risk_score"),
            blocked=source.get("blocked"))
        return user

    def to_dict(self) -> dict:
        user_dict = {
            "line_user_id": self.line_user_id,
            "line_user_pic_url": self.line_user_pic_url,
            "line_user_nickname": self.line_user_nickname,
            "line_user_status": self.line_user_status,
            "line_user_system_language": self.line_user_system_language,
            "line_bot_state": self.line_bot_state,
            "line_bot_history": self.line_bot_history,
            "user_risk_score": self.user_risk_score,
            "blocked": self.blocked}
        return user_dict
