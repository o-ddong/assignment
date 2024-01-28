
from django.db import models
from django.db.models import QuerySet, Q

from applications.base.models import TimeStampedModel
from applications.billings.constants import CategoryChoices, SizeChoices
from applications.billings.utils import convert_to_initials
from applications.users.models import User


class Product(TimeStampedModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="소유자")
    category = models.IntegerField(choices=CategoryChoices.CHOICES, default=CategoryChoices.OTHER, verbose_name="카테고리")
    price = models.IntegerField(verbose_name="가격")
    cost = models.IntegerField(verbose_name="원가")
    name = models.CharField(max_length=30, verbose_name="이름")
    description = models.TextField(verbose_name="설명")
    barcode = models.CharField(max_length=50, verbose_name="바코드")
    expire_date = models.DateField(verbose_name="유통기한")
    size = models.IntegerField(choices=SizeChoices.CHOICES, verbose_name="사이즈")

    @staticmethod
    def get_matching_products(search_name: str) -> QuerySet:
        # TODO: 초성 검증 추가 필요
        initials_keyword = convert_to_initials(search_name)
        return Product.objects.filter(Q(name__contains=search_name) | Q(name__contains=initials_keyword))
