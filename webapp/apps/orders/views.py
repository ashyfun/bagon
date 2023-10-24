import re
import asyncio

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from webapp.apps.orders import messages
from webapp.apps.orders.utils import send_message, send_group_message, create_order, get_order
from webapp.apps.orders.models import Order
from webapp.apps.orders.serializers import TelegramUserSerializer, OrderItemSerializer, OrderSerializer

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


class OrderList(APIView):

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_data = serializer.validated_data['tg_user']
        username = user_data['username']

        if not user_data['phone_number']:
            order = create_order(user_data, serializer.validated_data['items'])
            message = messages.ORDER_CREATED_MESSAGE.format(
                user_data['first_name'] + user_data['last_name'],
                f'@{username}' if username else '-',
                order.order_number,
                order,
            )
            async def run():
                await asyncio.gather(
                    send_message(user_data['user_id'], message),
                )
            loop.run_until_complete(run())
        else:
            order = get_order(user_data)
            message = messages.CUSTOMER_ORDER_MESSAGE.format(
                user_data['first_name'] + user_data['last_name'],
                order.order_number,
                user_data['phone_number'],
            )
            async def run():
                await asyncio.gather(
                    send_group_message(message),
                )
            loop.run_until_complete(run())
        return Response(status=status.HTTP_201_CREATED)
