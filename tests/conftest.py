import pytest
from django.contrib.auth.hashers import make_password
from django.urls import reverse

from applications.base.crypto import AESCipher
from applications.base.jwt_utils import generate_jwt
from applications.billings.constants import CategoryChoices, SizeChoices
from applications.billings.models import Product
from applications.users.models import User


pytestmark = pytest.mark.django_db

cipher = AESCipher()


USER_NAEM = "오동훈"
SAMPLE_MDN = "01012345678"
SAMPLE_SECOND_MDN = "01000001111"
SAMPLE_10_DIGIT_MDN = "0101234567"
SAMPLE_15_DIGIT_MDN = "0101234567891234"
SAMPLE_11_ENG_DATA = "aaaaabbbbbc"

SAMPLE_PASSWORD = "test1234!!"
SAMPLE_SECOND_PASSWORD = "second1234!!"


@pytest.fixture
def sample_user():
    """ 첫 번째 유저 데이터 샘플 """
    return User.objects.create(
        name=USER_NAEM,
        mdn=cipher.encrypt_str(SAMPLE_MDN),
        password=make_password(SAMPLE_PASSWORD)
    )

@pytest.fixture
def sample_second_user():
    """ 두 번째 유저 데이터 샘플 """
    return User.objects.create(
        name=USER_NAEM,
        mdn=cipher.encrypt_str(SAMPLE_SECOND_MDN),
        password=SAMPLE_PASSWORD
    )


@pytest.fixture
def sample_product(sample_user):
    """ 상품 데이터 샘플 """
    return Product.objects.create(
        user=sample_user,
        category=CategoryChoices.COFFEE,
        price=1000,
        cost=1000,
        name="아메리카노",
        description="아메라카노",
        barcode="barcode test",
        expire_date="2024-01-31",
        size=SizeChoices.SMALL,
    )


@pytest.fixture
def sample_create_jwt(sample_user):
    """ JWT 토큰 샘플 """
    access_token = generate_jwt(sample_user.id, 2)
    refresh_token = generate_jwt(sample_user.id, 4)

    return access_token, refresh_token


@pytest.fixture
def sample_create_expired_jwt(sample_user):
    """ 만료된 JWT 토큰 샘플 """
    expired_access_token = generate_jwt(sample_user.id, -4)
    expired_refresh_token = generate_jwt(sample_user.id, -6)

    return expired_access_token, expired_refresh_token

