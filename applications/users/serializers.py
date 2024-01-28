from rest_framework import serializers

from applications.base.crypto import AESCipher
from applications.base.messages import user_paramter_validation_message, user_mdn_validation_message
from applications.users.models import User
from applications.users.utils import mdn_asterisk


cipher = AESCipher()


class UserValidation:
    @staticmethod
    def validate_mdn(mdn):
        if not mdn:
            raise serializers.ValidationError(user_paramter_validation_message)

        if len(mdn) != 11:
            raise serializers.ValidationError(user_mdn_validation_message)

        if any(num.isalpha() for num in mdn):
            raise serializers.ValidationError(user_mdn_validation_message)

        return mdn

    @staticmethod
    def validate_password(password):
        if not password:
            raise serializers.ValidationError(user_paramter_validation_message)

        return password


class UserSerializer(serializers.ModelSerializer):

    mdn = serializers.CharField(max_length=11, required=True, validators=[UserValidation.validate_mdn])
    password = serializers.CharField(max_length=128, write_only=True, validators=[UserValidation.validate_password])

    class Meta:
        model = User
        fields = ['mdn', 'password']


class UserMdnTinySerializer(serializers.ModelSerializer):
    mdn = serializers.SerializerMethodField()

    def get_mdn(self, obj):
        return mdn_asterisk(cipher.decrypt_str(obj.mdn))

    class Meta:
        model = User
        fields = ['mdn']
