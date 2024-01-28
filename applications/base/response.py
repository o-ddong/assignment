from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response


operation_success = Response(
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
invalid_mdn = Response(
    status=status.HTTP_400_BAD_REQUEST,
    data={"meta": {"code": status.HTTP_400_BAD_REQUEST, "message": "INVALID_MDN"}, "data": ""}
)
required_field = Response(
    status=status.HTTP_400_BAD_REQUEST,
    data={"meta": {"code": status.HTTP_400_BAD_REQUEST, "message": "REQUIRED_FIELD_NOT_ENTERED"}, "data": ""}
)
authorization_error = Response(
    status=status.HTTP_401_UNAUTHORIZED,
    data={"meta": {"code": status.HTTP_401_UNAUTHORIZED, "message": "AUTHORIZATION_ERROR"}, "data": ""}
)


# middleware error
middle_authorization_error = JsonResponse(
    status=status.HTTP_401_UNAUTHORIZED, data={"message": "AUTHORIZATION_ERROR"}
)
expired_token = JsonResponse(
    status=status.HTTP_403_FORBIDDEN, data={"message": "EXPIRED_TOKEN"}
)