'''
負責與db溝通
save_user(user:User) :新增資料時，若有重複資料，則採更新
get_user(user_id:str):取用資料，開放以user_id的方式尋找
'''

import os
import sqlite3

from models import User


# Initiate the database
if "users" not in os.listdir():
    os.makedirs("users/pics")
con = sqlite3.connect("users/users.db")
cur = con.cursor()
res = cur.execute("SELECT name FROM sqlite_master").fetchone()
if not res or "users" not in res:
    cur.execute(
        "CREATE TABLE users(line_user_id, line_user_pic_url, line_user_nickname, line_user_status, "
        "line_user_system_language, line_bot_state, line_bot_history, user_risk_score, blocked)")
con.close()


class UserDAO:
    # 新增資料時，若有重複資料，則採更新
    @classmethod
    def save_user(cls, user: User) -> dict:
        # print(user)

        # 查找用戶資料
        con = sqlite3.connect("users/users.db")
        cur = con.cursor()
        res = cur.execute("SELECT * FROM users WHERE line_user_id = ?", (user.line_user_id,)).fetchone()

        # 檢查用戶資料是否存在
        if res:  # 更新
            cur.execute("UPDATE users SET line_user_pic_url = ?, line_user_nickname = ?, "
                        "line_user_status = ?, line_user_system_language = ?, "
                        "line_bot_state = ?, line_bot_history = ?, user_risk_score = ?, "
                        "blocked = ? WHERE line_user_id = ?",
                        tuple([v for v in user.to_dict().values()][1:] + [user.line_user_id]))
            con.commit()
            print("has already update")
        else:  # 直接插入
            cur.executemany("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            [tuple([v for v in user.to_dict().values()])])
            con.commit()
            print("No such document!")
        con.close()
        return user.to_dict()

    # 取用資料，開放以user_id的方式尋找
    @classmethod
    def get_user(cls, user_id: str) -> User:

        # 設定要查找的資料
        con = sqlite3.connect("users/users.db")
        cur = con.cursor()
        res = cur.execute("SELECT * FROM users WHERE line_user_id = ?", (user_id,)).fetchone()

        # 若資料存在
        if res:
            user = User(
                line_user_id=res[0],
                line_user_pic_url=res[1],
                line_user_nickname=res[2],
                line_user_status=res[3],
                line_user_system_language=res[4],
                line_bot_state=res[5],
                line_bot_history=res[6],
                user_risk_score=res[7],
                blocked=res[8]
            )
            return user
        else:
            pass
        con.close()