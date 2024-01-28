from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from applications.base.models import TimeStampedModel


class UserManager(BaseUserManager):
    def create_user(self, mdn, password, **extra_fields):
        user = self.model(mdn=mdn, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, TimeStampedModel):
    name = models.CharField(max_length=15, verbose_name="이름")
    mdn = models.CharField(max_length=11, unique=True, verbose_name="전화번호")
    is_active = models.BooleanField(default=True, verbose_name="활성화 여부")

    objects = UserManager()

    USERNAME_FIELD = 'mdn'
    def __str__(self):
        return self.mdn
    class Meta:
        db_table = 'user'
