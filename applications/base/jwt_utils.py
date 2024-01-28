from datetime import datetime, timedelta

import jwt
from django.conf import settings


def generate_jwt(user_id: int, expires_in_weeks: int) -> dict:
    iat = datetime.now()
    expired_date = iat + timedelta(weeks=expires_in_weeks)

    payload = {
        "user_id": user_id,
        "expired": expired_date.strftime("%Y-%m-%d %H:%M:%S"),
        "iat": iat.timestamp(),
    }

    return jwt.encode(payload, settings.SECRET_KEY, "HS256")


def decode_jwt(token: str) -> dict or None:
    try:
        return jwt.decode(token, settings.SECRET_KEY, "HS256")
    except:
        return None


def check_jwt_expired_date(now_date: str, expired_date: str) -> bool:
    now_date = datetime.strptime(now_date, "%Y-%m-%d %H:%M:%S")
    expired_date = datetime.strptime(expired_date, "%Y-%m-%d %H:%M:%S")

    if expired_date <= now_date:
        return True
    else:
        return False


def check_jwt_equality(access_token: str, refresh_token: str) -> dict or None:
    access_token_payload = decode_jwt(access_token)
    refresh_token_payload = decode_jwt(refresh_token)

    if access_token_payload and refresh_token_payload:
        access_token_user_id = access_token_payload.get("user_id", None)
        refresh_token_user_id = refresh_token_payload.get("user_id", None)

        if access_token_user_id == refresh_token_user_id:
            new_access_token = generate_jwt(access_token_user_id, expires_in_weeks=2)
            new_refresh_token = generate_jwt(refresh_token_user_id, expires_in_weeks=4)

            results = {"access_token": new_access_token, "refresh_token": new_refresh_token}
            return results
        else:
            return None
    else:
        return None
