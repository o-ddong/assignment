from rest_framework import serializers

from applications.base.messages import user_paramter_validation_message, user_mdn_validation_message
from applications.users.models import User


class MdnSerializer(serializers.ModelSerializer):
    mdn = serializers.CharField(max_length=11, required=True)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate_password(self, password):
        if not password:
            raise serializers.ValidationError(user_paramter_validation_message)

        return password

    def validate_mdn(self, mdn):
        print("==== start validate mdn ====")
        if not mdn:
            raise serializers.ValidationError(user_paramter_validation_message)

        if len(mdn) != 11:
            raise serializers.ValidationError(user_mdn_validation_message)

        if any(num.isalpha() for num in mdn):
            raise serializers.ValidationError(user_mdn_validation_message)

        print("==== end validate mdn ====")
        return mdn

    class Meta:
        model = User
        fields = ['mdn', 'password']
