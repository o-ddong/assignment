import traceback

from django.contrib.auth import logout, login
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError

from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from applications.base.crypto import AESCipher
from applications.base.jwt_utils import generate_jwt, check_jwt_equality
from applications.base.messages import user_paramter_validation_message, user_mdn_validation_message, \
    common_validation_message
from applications.base.response import operation_success, authorization_error, operation_failure, already_exist_user, \
    invalid_mdn_format, invaild_required_field, same_data_failure, invalid_token
from applications.users.models import User
from applications.users.serializers import UserSerializer


cipher = AESCipher()


class UsersViewSet(GenericViewSet):
    queryset = User.objects.all().order_by('-id')

    @action(methods=['POST'], detail=False)
    def login(self, request, *args, **kwargs):
        mdn = request.data.get('mdn')
        password = request.data.get('password')

        try:
            user = User.objects.get(mdn=cipher.encrypt_str(mdn))
            password_matched = check_password(password, user.password)
            if password_matched:
                login(request, user)
                return operation_success
            else:
                return authorization_error

        except User.DoesNotExist:
            return authorization_error

        except Exception:
            traceback.print_exc()
            return operation_failure

    @action(methods=['POST'], detail=False)
    def logout(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return operation_success
        else:
            return operation_failure

    @action(methods=['POST'], detail=False)
    def join(self, request, *args, **kwargs):
        mdn = request.data.get('mdn')
        password = request.data.get('password')

        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors

            if 'mdn' in errors:
                for mdn_error in errors['mdn']:
                    if common_validation_message in mdn_error:
                        return invaild_required_field

                    if user_paramter_validation_message in mdn_error:
                        return invaild_required_field

                    if user_mdn_validation_message in mdn_error:
                        return invalid_mdn_format

            elif 'password' in errors:
                for password_error in errors['password']:
                    if common_validation_message in password_error:
                        return invaild_required_field

                    if user_paramter_validation_message in password_error:
                        return invaild_required_field

        try:
            user = User.objects.create_user(mdn, password)
            if user:
                access_token = generate_jwt(user.id, expires_in_weeks=2)
                refresh_token = generate_jwt(user.id, expires_in_weeks=4)

                response = operation_success
                response.data["data"] = {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
                return response

        except IntegrityError:
            traceback.print_exc()
            return already_exist_user

        except ValueError:
            return operation_failure

    @action(methods=['POST'], detail=False, url_path="refresh_token")
    def jwt_refresh_token(self, request, *args, **kwargs):
        access_token = request.data.get("access_token", None)
        refresh_token = request.data.get("refresh_token", None)

        if access_token == refresh_token:
            return same_data_failure

        results = check_jwt_equality(access_token, refresh_token)
        if not results:
            return invalid_token

        response = operation_success
        response.data["data"] = results

        return response
