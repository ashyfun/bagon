from rest_framework import serializers


class TelegramUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField(max_length=32)
    first_name = serializers.CharField(max_length=64)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=64)


class OrderSerializer(serializers.Serializer):
    tg_user = TelegramUserSerializer()
    name = serializers.CharField()
    price = serializers.CharField()
    amount = serializers.IntegerField(default=1)
