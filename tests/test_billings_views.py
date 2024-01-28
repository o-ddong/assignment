import pytest

from django.urls import reverse
from rest_framework import status

from applications.base.crypto import AESCipher
from applications.base.jwt_utils import generate_jwt
from applications.base.response import operation_success, invaild_required_field, middle_authorization_error, \
    not_found_data, ProductNotFound

pytestmark = pytest.mark.django_db

cipher = AESCipher()


def test_get_product_list(client, sample_create_jwt):
    """ 상품 조회 테스트 - 성공 """
    access_token, refresh_token = sample_create_jwt

    header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    join_url = reverse("product-list")

    response = client.get(path=join_url, **header)

    assert response.data['meta']['code'] == operation_success.data["meta"]["code"]
    assert response.data['meta']['message'] == operation_success.data["meta"]["message"]


def test_get_product_list_without_jwt(client):
    """ 상품 상세 조회 테스트 (jwt 제외) - 성공 """
    join_url = reverse("product-list")

    response = client.get(path=join_url)

    assert response.status_code == middle_authorization_error.status_code


def test_product_create_success(client, sample_create_jwt):
    """ 상품 생성 테스트 - 성공 """
    access_token, refresh_token = sample_create_jwt

    header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    join_url = reverse("product-list")
    data = {
        "category": "커피",
        "price": 1000,
        "cost": 1000,
        "name": "아메리카노",
        "description": "커피류",
        "barcode": "11223344",
        "expire_date": "2023-01-01",
        "size": "small"
    }

    response = client.post(path=join_url, data=data, **header)

    assert response.data['meta']['code'] == operation_success.data["meta"]["code"]
    assert response.data['meta']['message'] == operation_success.data["meta"]["message"]


def test_product_create_without_category(client, sample_create_jwt):
    """ 상품 생성 테스트 (카테고리 누락) - 성공 """
    access_token, refresh_token = sample_create_jwt

    header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    join_url = reverse("product-list")
    data = {
        "price": 1000,
        "cost": 1000,
        "name": "아메리카노",
        "description": "커피류",
        "barcode": "11223344",
        "expire_date": "2023-01-01",
        "size": "small"
    }

    response = client.post(path=join_url, data=data, **header)

    assert response.data['meta']['code'] == invaild_required_field.data["meta"]["code"]
    assert response.data['meta']['message'] == invaild_required_field.data["meta"]["message"]


def test_product_create_without_price(client, sample_create_jwt):
    """ 상품 생성 테스트 (가격 누락) - 성공 """
    access_token, refresh_token = sample_create_jwt

    header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    join_url = reverse("product-list")
    data = {
        "category": "커피",
        "cost": 1000,
        "name": "아메리카노",
        "description": "커피류",
        "barcode": "11223344",
        "expire_date": "2023-01-01",
        "size": "small"
    }

    response = client.post(path=join_url, data=data, **header)

    assert response.data['meta']['code'] == invaild_required_field.data["meta"]["code"]
    assert response.data['meta']['message'] == invaild_required_field.data["meta"]["message"]


def test_product_create_without_cost(client, sample_create_jwt):
    """ 상품 생성 테스트 (원가 누락) - 성공 """
    access_token, refresh_token = sample_create_jwt

    header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    join_url = reverse("product-list")
    data = {
        "category": "커피",
        "price": 1000,
        "name": "아메리카노",
        "description": "커피류",
        "barcode": "11223344",
        "expire_date": "2023-01-01",
        "size": "small"
    }

    response = client.post(path=join_url, data=data, **header)

    assert response.data['meta']['code'] == invaild_required_field.data["meta"]["code"]
    assert response.data['meta']['message'] == invaild_required_field.data["meta"]["message"]


def test_product_create_without_name(client, sample_create_jwt):
    """ 상품 생성 테스트 (이름 누락) - 성공 """
    access_token, refresh_token = sample_create_jwt

    header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    join_url = reverse("product-list")
    data = {
        "category": "커피",
        "price": 1000,
        "cost": 1000,
        "description": "커피류",
        "barcode": "11223344",
        "expire_date": "2023-01-01",
        "size": "small"
    }

    response = client.post(path=join_url, data=data, **header)

    assert response.data['meta']['code'] == invaild_required_field.data["meta"]["code"]
    assert response.data['meta']['message'] == invaild_required_field.data["meta"]["message"]


def test_product_create_without_description(client, sample_create_jwt):
    """ 상품 생성 테스트 (설명 누락) - 성공 """
    access_token, refresh_token = sample_create_jwt

    header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    join_url = reverse("product-list")
    data = {
        "category": "커피",
        "price": 1000,
        "cost": 1000,
        "name": "아메리카노",
        "barcode": "11223344",
        "expire_date": "2023-01-01",
        "size": "small"
    }

    response = client.post(path=join_url, data=data, **header)

    assert response.data['meta']['code'] == invaild_required_field.data["meta"]["code"]
    assert response.data['meta']['message'] == invaild_required_field.data["meta"]["message"]


def test_product_create_without_barcode(client, sample_create_jwt):
    """ 상품 생성 테스트 (바코드 누락) - 성공 """
    access_token, refresh_token = sample_create_jwt

    header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    join_url = reverse("product-list")
    data = {
        "category": "커피",
        "price": 1000,
        "cost": 1000,
        "name": "아메리카노",
        "description": "커피류",
        "expire_date": "2023-01-01",
        "size": "small"
    }

    response = client.post(path=join_url, data=data, **header)

    assert response.data['meta']['code'] == invaild_required_field.data["meta"]["code"]
    assert response.data['meta']['message'] == invaild_required_field.data["meta"]["message"]


def test_product_create_without_expire_date(client, sample_create_jwt):
    """ 상품 생성 테스트 (유효기간 누락) - 성공 """
    access_token, refresh_token = sample_create_jwt

    header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    join_url = reverse("product-list")
    data = {
        "category": "커피",
        "price": 1000,
        "cost": 1000,
        "name": "아메리카노",
        "description": "커피류",
        "barcode": "11223344",
        "size": "small"
    }

    response = client.post(path=join_url, data=data, **header)

    assert response.data['meta']['code'] == invaild_required_field.data["meta"]["code"]
    assert response.data['meta']['message'] == invaild_required_field.data["meta"]["message"]


def test_product_create_without_size(client, sample_create_jwt):
    """ 상품 생성 테스트 (사이즈 누락) - 성공 """
    access_token, refresh_token = sample_create_jwt

    header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    join_url = reverse("product-list")
    data = {
        "category": "커피",
        "price": 1000,
        "cost": 1000,
        "name": "아메리카노",
        "description": "커피류",
        "barcode": "11223344",
        "expire_date": "2023-01-01",
    }

    response = client.post(path=join_url, data=data, **header)

    assert response.data['meta']['code'] == invaild_required_field.data["meta"]["code"]
    assert response.data['meta']['message'] == invaild_required_field.data["meta"]["message"]


def test_get_product_retrieve(client, sample_create_jwt, sample_product):
    """ 상품 상세 조회 테스트 - 성공 """
    access_token, refresh_token = sample_create_jwt

    header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    join_url = reverse("product-detail", kwargs={'pk': sample_product.id})

    response = client.get(path=join_url, **header)

    assert response.data['meta']['code'] == operation_success.data["meta"]["code"]
    assert response.data['meta']['message'] == operation_success.data["meta"]["message"]


def test_get_product_retrieve_without_jwt(client, sample_product):
    """ 상품 상세 조회 테스트 (jwt 제외) - 성공 """
    join_url = reverse("product-detail", kwargs={'pk': sample_product.id})

    response = client.get(path=join_url)

    assert response.status_code == middle_authorization_error.status_code


def test_get_product_retrieve_another_user(client, sample_product, sample_second_user):
    """ 상품 상세 조회 테스트 (다른 사용자) - 성공 """
    header = {"HTTP_AUTHORIZATION": f"Bearer {generate_jwt(sample_second_user.id, 2)}"}
    join_url = reverse("product-detail", kwargs={'pk': sample_product.id})

    response = client.get(path=join_url, **header)

    assert response.status_code == ProductNotFound.status_code


def test_update_product(client, sample_create_jwt, sample_product):
    """ 상품 업데이트 테스트 - 실패
    TODO: 수정 필요 (415 에러나는데 우선 pass)
    """
    access_token, refresh_token = sample_create_jwt

    header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    join_url = reverse("product-detail", kwargs={'pk': sample_product.id})
    data = {
        "category": "커피",
        "price": 10000,
        "cost": 10000,
        "name": "아메리카노",
        "description": "커피류",
        "barcode": "11223344",
        "expire_date": "2023-01-01",
        "size": "large"
    }

    response = client.put(path=join_url, data=data, **header)

    assert response.data['meta']['code'] == operation_success.data["meta"]["code"]
    assert response.data['meta']['message'] == operation_success.data["meta"]["message"]


def test_delete_product(client, sample_create_jwt, sample_product):
    """ 상품 삭제 테스트 - 성공 """
    access_token, refresh_token = sample_create_jwt

    header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    join_url = reverse("product-detail", kwargs={'pk': sample_product.id})

    response = client.delete(path=join_url, **header)

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_product_without_jwt(client, sample_product):
    """ 상품 삭제 테스트 (jwt 제외) - 성공 """
    join_url = reverse("product-detail", kwargs={'pk': sample_product.id})

    response = client.delete(path=join_url)

    assert response.status_code == middle_authorization_error.status_code


def test_search_product(client, sample_create_jwt, sample_product):
    """ 상품 검색 테스트 - 실패
    # TODO: 검색 기능 검토 필요
    """
    access_token, refresh_token = sample_create_jwt

    header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    data = {"name": "아메"}
    join_url = reverse("product-search")

    response = client.post(path=join_url, data=data, **header)

    assert response.data['meta']['code'] == operation_success.data["meta"]["code"]
    assert response.data['meta']['message'] == operation_success.data["meta"]["message"]


def test_search_product_no_data(client, sample_create_jwt, sample_product):
    """ 상품 검색 테스트 (해당하는 데이터가 없을 경우) - 성공 """
    access_token, refresh_token = sample_create_jwt

    header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    data = {"name": "아메리카노"}
    join_url = reverse("product-search")

    response = client.post(path=join_url, data=data, **header)

    assert response.data['meta']['code'] == not_found_data.data["meta"]["code"]
    assert response.data['meta']['message'] == not_found_data.data["meta"]["message"]


def test_search_product_without_name(client, sample_create_jwt, sample_product):
    """ 상품 검색 테스트 (상품 이름 누락) - 성공 """
    access_token, refresh_token = sample_create_jwt

    header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    join_url = reverse("product-search")

    response = client.post(path=join_url, **header)

    assert response.data['meta']['code'] == invaild_required_field.data["meta"]["code"]
    assert response.data['meta']['message'] == invaild_required_field.data["meta"]["message"]


def test_search_product_without_jwt(client, sample_product):
    """ 상품 검색 테스트 (jwt 제외) - 성공 """
    join_url = reverse("product-search")
    data = {"name": "아메리카노"}

    response = client.post(path=join_url, data=data)

    assert response.status_code == middle_authorization_error.status_code
