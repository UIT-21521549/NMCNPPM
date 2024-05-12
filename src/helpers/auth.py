from functools import wraps
from flask import request
from src.database import USER
from flask import g

def auth_decorator(admin_only=False):
    # admin_only: if true, only admin user can use this endpoint

    def _auth_decorator(f):
        @wraps(f)
        def __auth_decorator(*args, **kwargs):

            token = request.cookies.get("session_token")
            
            if token is None:
                try:
                    data = request.get_json(force=True)
                except:
                    return "session_token needed", 400
                
                if "session_token" not in data.keys():
                    return "session_token needed", 400
                
                token = data["session_token"]

            payload = USER.verify_jwt_token(token)

            if admin_only and not payload["is_admin"]:
                return "Forbidden access", 403

            g.user_id = payload["user_id"]
            g.is_admin = payload["is_admin"]

            result = f(*args, **kwargs)
            return result
        return __auth_decorator
    return _auth_decorator