from rest_framework import serializers


class TelegramUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=32)
    first_name = serializers.CharField(max_length=64)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=64)
    phone_number = serializers.CharField(max_length=15)


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.CharField()
    amount = serializers.IntegerField(default=1)


class OrderSerializer(serializers.Serializer):
    tg_user = TelegramUserSerializer()
    products = ProductSerializer(many=True)
