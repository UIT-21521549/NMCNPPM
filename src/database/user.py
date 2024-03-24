from sqlalchemy import select
import jwt
import os
from datetime import datetime, timezone, timedelta


class User:
    def __init__(self, db_engine):
        self.db_engine = db_engine

    def verify(self, username, password):
        """check if username and password pair is corrected"""
        if username is None or password is None:
            return None

        # TODO: sanitize user input
        query = f"SELECT acc,pass,acess FROM login_user WHERE acc='{username}' AND password='{password}'"

        with self.db_engine.connect() as conn:
            result = conn.execute(query)

        if len(result) == 0:
            return None

        # assume username and password pair is unique

        username, password, access = result[0]

        return username, password, access

    def check_username(self, username):
        if username is None:
            return False

        # TODO: sanitize user input
        query = f"SELECT acc FROM login_user WHERE acc='{username}'"

        with self.db_engine.connect() as conn:
            result = conn.execute(query)

        if len(result) == 0:
            return False

        return True

    def register(self, username, password):

        already_existed = self.check_username(username)

        if already_existed:
            return False

        # TODO: sanitize user input and only store password hash
        query = f"insert INTO login_user(acc,pass,acess) values ('{username}', '{password}', 'user')"

        with self.db_engine.connect() as conn:
            conn.execute(query)
            # TODO: check if success
            conn.commit()

        return True

    def get_jwt_token(self, username, password):

        jwt_secret = os.getenv("jwt_secret")
        assert jwt_secret is not None

        user = self.verify(username, password)
        if user is None:
            return None

        username, password, access = user

        payload = {
            "username": username,
            "access": access,
            # hết hạng sau 1 ngày
            "exp": datetime.now(tz=timezone.utc) + timedelta(days=1),
        }

        token = jwt.encode(payload, jwt_secret, algorithm="HS256")

        return token

    def verify_jwt_token(self, token):
        jwt_secret = os.getenv("jwt_secret")
        assert jwt_secret is not None

        try:
            payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        except e:
            print(e)
            return False, None

        return True, payload["username"], payload["access"]
