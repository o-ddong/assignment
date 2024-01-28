from django.http import JsonResponse
from rest_framework import status


# middleware error
middle_authorization_error = JsonResponse(
    status=status.HTTP_401_UNAUTHORIZED, data={"message": "AUTHORIZATION_ERROR"}
)
expired_token = JsonResponse(
    status=status.HTTP_403_FORBIDDEN, data={"message": "EXPIRED_TOKEN"}
)