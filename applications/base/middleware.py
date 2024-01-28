from datetime import datetime

from jwt import ExpiredSignatureError
from rest_framework.exceptions import PermissionDenied

from applications.base.jwt_utils import check_jwt_expired_date, decode_jwt
from applications.base.response import middle_authorization_error, expired_token


class JsonWebTokenMiddleWare(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if (
                request.path != "/v1/user/join"
                and request.path != "/v1/user/login"
                and "admin" not in request.path
            ):
                access_token = request.headers.get("Authorization", None)
                if not access_token:
                    raise PermissionDenied()

                auth_type, token = access_token.split(" ")
                if auth_type == "Bearer":
                    payload = decode_jwt(token)
                    if not payload:
                        raise PermissionDenied("permission denied")

                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    token_expired = payload.get("expired")

                    if check_jwt_expired_date(now, token_expired):
                        raise ExpiredSignatureError()

                    user_id = payload.get("user_id", None)
                    if not user_id:
                        raise PermissionDenied()

                else:
                    raise PermissionDenied()

            response = self.get_response(request)
            return response

        except ValueError:
            return middle_authorization_error

        except PermissionDenied:
            return middle_authorization_error

        except ExpiredSignatureError:
            return expired_token
