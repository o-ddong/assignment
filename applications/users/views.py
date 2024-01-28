import traceback

from django.contrib.auth import logout, login
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from applications.base.jwt_utils import generate_jwt
from applications.base.messages import user_paramter_validation_message, user_mdn_validation_message
from applications.base.response import operation_success, authorization_error, operation_failure, already_exist_user,\
    invalid_mdn, required_field
from applications.users.models import User
from applications.users.serializers import MdnSerializer


class UsersViewSet(GenericViewSet):
    queryset = User.objects.all().order_by('-id')

    @action(methods=['POST'], detail=False)
    def login(self, request, *args, **kwargs):
        mdn = request.data.get('mdn')
        password = request.data.get('password')

        try:
            user = User.objects.get(mdn=mdn)
            password_matched = check_password(password, user.password)
            if password_matched:
                login(request, user)

                return operation_success

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

        serializer = MdnSerializer(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors['non_field_errors'][0]

            if user_paramter_validation_message in errors:
                return required_field

            if user_mdn_validation_message in errors:
                return invalid_mdn

        try:
            user = User.objects.create_user(mdn, password)
            if user:
                access_token = generate_jwt(user.id, expires_in_weeks=2)
                refresh_token = generate_jwt(user.id, expires_in_weeks=4)

                response = operation_success.data
                response["data"] = {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
                return Response(status=200)

        except IntegrityError:
            traceback.print_exc()
            return already_exist_user

        except ValueError:
            return operation_failure


