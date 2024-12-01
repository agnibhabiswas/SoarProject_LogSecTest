import jwt

def decode_jwt(token, secret_key=None):
    try:
        return jwt.decode(token, secret=secret_key, algorithms=["HS256"], options={"verify_signature": False})
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
