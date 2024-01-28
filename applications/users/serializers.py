from rest_framework import serializers

from applications.base.messages import user_paramter_validation_message, user_mdn_validation_message
from applications.users.models import User


class MdnSerializer(serializers.ModelSerializer):
    mdn = serializers.CharField(max_length=11)

    def validate(self, attrs):
        mdn = attrs.get('mdn')
        password = attrs.get('password')

        if not mdn or not password:
            raise serializers.ValidationError(user_paramter_validation_message)

        if len(mdn) != 11:
            raise serializers.ValidationError(user_mdn_validation_message)

        return attrs

    class Meta:
        model = User
        fields = ['mdn', ]
