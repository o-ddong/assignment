from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response


operation_success = Response(
    status=status.HTTP_200_OK,
    data={"meta": {"code": status.HTTP_200_OK, "message": "OK"}, "data": ""}
)
create_success = Response(
    status=status.HTTP_200_OK,
    data={"meta": {"code": status.HTTP_200_OK, "message": "OK"}, "data": ""}
)
operation_failure = Response(
    status=status.HTTP_400_BAD_REQUEST,
    data={"meta": {"code": status.HTTP_400_BAD_REQUEST, "message": ""}, "data": ""}
)
already_exist_user = Response(
    status=status.HTTP_400_BAD_REQUEST,
    data={"meta": {"code": status.HTTP_400_BAD_REQUEST, "message": "ALREADY_EXIST_USER"}, "data": ""}
)
invalid_token = Response(
    status=status.HTTP_400_BAD_REQUEST,
    data={"meta": {"code": status.HTTP_400_BAD_REQUEST, "message": "INVALID_TOKEN"}, "data": ""}
)
same_data_failure = Response(
    status=status.HTTP_400_BAD_REQUEST,
    data={"meta": {"code": status.HTTP_400_BAD_REQUEST, "message": "SAME_DATA_FAILURE"}, "data": ""}
)
invalid_mdn_format = Response(
    status=status.HTTP_400_BAD_REQUEST,
    data={"meta": {"code": status.HTTP_400_BAD_REQUEST, "message": "INVALID_MDN_FORMAT"}, "data": ""}
)
invaild_required_field = Response(
    status=status.HTTP_400_BAD_REQUEST,
    data={"meta": {"code": status.HTTP_400_BAD_REQUEST, "message": "INVALID_REQUIRED_FIELD"}, "data": ""}
)
authorization_error = Response(
    status=status.HTTP_401_UNAUTHORIZED,
    data={"meta": {"code": status.HTTP_401_UNAUTHORIZED, "message": "AUTHORIZATION_ERROR"}, "data": ""}
)
not_found_data = Response(
    status=status.HTTP_401_UNAUTHORIZED,
    data={"meta": {"code": status.HTTP_404_NOT_FOUND, "message": "NOT_FOUND_DATA"}, "data": ""}
)


# middleware error
middle_authorization_error = JsonResponse(
    status=status.HTTP_401_UNAUTHORIZED, data={"message": "AUTHORIZATION_ERROR"}
)
expired_token = JsonResponse(
    status=status.HTTP_403_FORBIDDEN, data={"message": "EXPIRED_TOKEN"}
)


# raise handler
class ProductNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = {"message": "해당하는 상품이 없습니다."}
    default_code = 'not_found'


class ProductPermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {"message": "해당 상품에 접근 권한이 없습니다."}
    default_code = 'permission_denied'


