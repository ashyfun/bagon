from rest_framework import serializers

from webapp.apps.orders.models import OrderItem


class TelegramUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField(required=False, allow_blank=True, max_length=32)
    first_name = serializers.CharField(max_length=64)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=64)
    phone_number = serializers.CharField(required=False, allow_blank=True, max_length=15)


class OrderItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    size = serializers.CharField(max_length=2, default=OrderItem.Size.S)
    color = serializers.CharField(max_length=32)
    price = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)


class OrderSerializer(serializers.Serializer):
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    tg_user = TelegramUserSerializer()
    items = OrderItemSerializer(many=True)
