from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from applications.base.crypto import AESCipher
from applications.base.models import TimeStampedModel
from applications.users.utils import mdn_asterisk

cipher = AESCipher()


class UserManager(BaseUserManager):
    def create_user(self, mdn: str, password: str, **extra_fields) -> object:
        user = self.model(mdn=cipher.encrypt_str(mdn), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, TimeStampedModel):
    name = models.CharField(max_length=15, verbose_name="이름")
    mdn = models.CharField(max_length=64, unique=True, verbose_name="전화번호")
    is_active = models.BooleanField(default=True, verbose_name="활성화 여부")

    objects = UserManager()

    USERNAME_FIELD = 'mdn'

    def __str__(self):
        return mdn_asterisk(cipher.decrypt_str(self.mdn))

    class Meta:
        db_table = 'user'
