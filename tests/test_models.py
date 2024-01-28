import pytest
from django.db import IntegrityError

from applications.base.crypto import AESCipher
from applications.billings.constants import CategoryChoices, SizeChoices
from applications.billings.models import Product
from applications.users.models import User
from tests.conftest import SAMPLE_MDN, SAMPLE_PASSWORD

pytestmark = pytest.mark.django_db

cipher = AESCipher()


def test_user_model_create():
    """ mdn, password 가지고 있는 유저 생성 - 성공 """
    user = User.objects.create(
        name="오동훈",
        mdn=cipher.encrypt_str(SAMPLE_MDN),
        password=SAMPLE_PASSWORD
    )

    assert user.name == "오동훈"
    assert str(user) == "01012**56**"


def test_already_create_same_user(sample_user):
    """ mdn 동일한 유저 생성 확인 (IntegrityError 발생) - 성공 """
    with pytest.raises(IntegrityError):
        user = User.objects.create(
            name="오동훈",
            mdn=cipher.encrypt_str(SAMPLE_MDN),
            password=SAMPLE_PASSWORD
        )


def test_product_model_create(sample_user):
    """ 상품 생성 확인 - 성공 """
    product = Product.objects.create(
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

    assert product.user == sample_user
    assert product.name == "아메리카노"
