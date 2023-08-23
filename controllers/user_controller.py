from flask import Request, Response
# import json

from services import UserService


class UserController:

    @classmethod
    def get_user(cls, request: Request) -> dict:
        user_id = request.args.get('line_user_id')
        user = UserService.get_user(user_id)
        return user.to_dict()
