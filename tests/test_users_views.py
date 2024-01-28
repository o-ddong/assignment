import pytest

from django.urls import reverse

from applications.base.crypto import AESCipher
from applications.base.jwt_utils import generate_jwt
from applications.base.response import operation_success, invaild_required_field, invalid_mdn_format, \
    already_exist_user, same_data_failure, invalid_token, authorization_error, expired_token

from tests.conftest import SAMPLE_MDN, SAMPLE_PASSWORD, SAMPLE_10_DIGIT_MDN, SAMPLE_15_DIGIT_MDN, SAMPLE_11_ENG_DATA, \
    SAMPLE_SECOND_PASSWORD

pytestmark = pytest.mark.django_db

cipher = AESCipher()


def test_user_join(client):
    """ 유저 생성 테스트 - 성공 """
    join_url = reverse("user-join")
    date = {
        "mdn": SAMPLE_MDN,
        "password": SAMPLE_PASSWORD
    }
    response = client.post(path=join_url, data=date)

    assert response.data['meta']['code'] == operation_success.data["meta"]["code"]
    assert response.data['meta']['message'] == operation_success.data["meta"]["message"]


def test_user_join_without_mdn(client):
    """ 유저 mdn 제외 생성 테스트 - 성공 """
    join_url = reverse("user-join")
    date = {
        "password": SAMPLE_PASSWORD,
    }
    response = client.post(path=join_url, data=date)

    assert response.data['meta']['code'] == invaild_required_field.data["meta"]["code"]
    assert response.data['meta']['message'] == invaild_required_field.data["meta"]["message"]


def test_user_join_without_password(client):
    """ 유저 mdn 제외 생성 테스트 - 성공 """
    join_url = reverse("user-join")
    date = {
        "mdn": SAMPLE_MDN,
    }
    response = client.post(path=join_url, data=date)

    assert response.data['meta']['code'] == invaild_required_field.data["meta"]["code"]
    assert response.data['meta']['message'] == invaild_required_field.data["meta"]["message"]


def test_user_mdn_10_digit(client):
    """ 유저 mdn 10자리 테스트 - 성공 """
    join_url = reverse("user-join")
    date = {
        "mdn": SAMPLE_10_DIGIT_MDN,
    }
    response = client.post(path=join_url, data=date)

    assert response.data['meta']['code'] == invalid_mdn_format.data["meta"]["code"]
    assert response.data['meta']['message'] == invalid_mdn_format.data["meta"]["message"]


def test_user_mdn_15_digit(client):
    """ 유저 mdn 15자리 테스트 - 성공 """
    join_url = reverse("user-join")
    date = {
        "mdn": SAMPLE_15_DIGIT_MDN,
    }
    response = client.post(path=join_url, data=date)

    assert response.data['meta']['code'] == invalid_mdn_format.data["meta"]["code"]
    assert response.data['meta']['message'] == invalid_mdn_format.data["meta"]["message"]


def test_user_mdn_eng_digit_digit(client):
    """ 유저 mdn 영어 테스트 - 성공 """
    join_url = reverse("user-join")
    date = {
        "mdn": SAMPLE_11_ENG_DATA,
    }
    response = client.post(path=join_url, data=date)

    assert response.data['meta']['code'] == invalid_mdn_format.data["meta"]["code"]
    assert response.data['meta']['message'] == invalid_mdn_format.data["meta"]["message"]


def test_already_create_user(client, sample_user):
    """ 동일한 유저 생성 테스트 - 성공 """
    join_url = reverse("user-join")
    date = {
        "mdn": SAMPLE_MDN,
        "password": SAMPLE_PASSWORD
    }
    response = client.post(path=join_url, data=date)

    assert response.data['meta']['code'] == already_exist_user.data["meta"]["code"]
    assert response.data['meta']['message'] == already_exist_user.data["meta"]["message"]


def test_user_login(client, sample_create_jwt):
    """ 유저 로그인 테스트 - 성공 """
    access_token, refresh_token = sample_create_jwt

    header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    join_url = reverse("user-login")

    date = {
        "mdn": SAMPLE_MDN,
        "password": SAMPLE_PASSWORD
    }
    response = client.post(path=join_url, data=date, **header)

    assert response.data['meta']['code'] == operation_success.data["meta"]["code"]
    assert response.data['meta']['message'] == operation_success.data["meta"]["message"]


def test_user_login_diff_password(client, sample_create_jwt):
    """ 유저 로그인 실패 테스트 (상이한 비밀번호) - 성공 """
    access_token, refresh_token = sample_create_jwt

    header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    join_url = reverse("user-login")

    date = {
        "mdn": SAMPLE_MDN,
        "password": SAMPLE_SECOND_PASSWORD
    }
    response = client.post(path=join_url, data=date, **header)

    assert response.data['meta']['code'] == authorization_error.data["meta"]["code"]
    assert response.data['meta']['message'] == authorization_error.data["meta"]["message"]


def test_user_login_with_expired_jwt(client, sample_create_expired_jwt):
    """ 유저 로그인 실패 테스트 (jwt 토큰 기간 만료) - 성공 """
    access_token, refresh_token = sample_create_expired_jwt

    header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    join_url = reverse("user-login")

    date = {
        "mdn": SAMPLE_MDN,
        "password": SAMPLE_SECOND_PASSWORD
    }
    response = client.post(path=join_url, data=date, **header)

    assert response.status_code == expired_token.status_code


def test_user_logout(client, sample_create_jwt):
    """ 유저 로그아웃 테스트 - 성공 """
    access_token, refresh_token = sample_create_jwt

    header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    join_url = reverse("user-logout")

    response = client.post(path=join_url, **header)

    assert response.data['meta']['code'] == operation_success.data["meta"]["code"]
    assert response.data['meta']['message'] == operation_success.data["meta"]["message"]


def test_refresh_jwt(client, sample_create_jwt):
    """ jwt refresh api 테스트 - 성공 """
    join_url = reverse("user-jwt-refresh-token")

    access_token, refresh_token = sample_create_jwt
    date = {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
    response = client.post(path=join_url, data=date)

    assert response.data['meta']['code'] == operation_success.data["meta"]["code"]
    assert response.data['meta']['message'] == operation_success.data["meta"]["message"]


def test_refresh_jwt_with_same_value(client, sample_create_jwt):
    """ jwt refresh api 테스트 (access, refresh token 동일한 데이터) - 성공 """
    join_url = reverse("user-jwt-refresh-token")

    access_token, refresh_token = sample_create_jwt
    date = {
        "access_token": access_token,
        "refresh_token": access_token
    }
    response = client.post(path=join_url, data=date)

    assert response.data['meta']['code'] == same_data_failure.data["meta"]["code"]
    assert response.data['meta']['message'] == same_data_failure.data["meta"]["message"]


def test_refresh_jwt_with_diff_value(client, sample_create_jwt, sample_second_user):
    """ jwt refresh api 테스트 (access, refresh token 동일한 데이터) - 성공 """
    join_url = reverse("user-jwt-refresh-token")

    access_token, refresh_token = sample_create_jwt
    date = {
        "access_token": access_token,
        "refresh_token": generate_jwt(sample_second_user.id, 4)
    }
    response = client.post(path=join_url, data=date)

    assert response.data['meta']['code'] == invalid_token.data["meta"]["code"]
    assert response.data['meta']['message'] == invalid_token.data["meta"]["message"]
