from functools import wraps
from flask import request
from src.database import USER
from flask import g, make_response

def auth_decorator(admin_only=False, logged_in_required=True):
    # admin_only: if true, only admin user can use this endpoint

    def _auth_decorator(f):
        @wraps(f)
        def __auth_decorator(*args, **kwargs):
            g.logged_in = False

            token = request.cookies.get("session_token")
            
            if token is None:
                try:
                    data = request.get_json(force=True)

                    assert "session_token" in data.keys()

                    token = data["session_token"]
                except:
                    if logged_in_required or admin_only:
                        return "session_token needed", 400
            
            if token is not None:
                try:
                    payload = USER.verify_jwt_token(token)
                except:
                    resp = make_response("session token expired!")
                    
                    # resp.delete_cookie('session_token')

                    return resp, 404

                if admin_only and not payload["is_admin"]:
                    return "you can't be here", 404

                g.user_id = payload["user_id"]
                g.is_admin = payload["is_admin"]
                g.logged_in = True

            result = f(*args, **kwargs)
            return result
        return __auth_decorator
    return _auth_decorator