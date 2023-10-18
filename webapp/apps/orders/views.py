import re
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from webapp.apps.orders.models import TelegramUserModel, ProductModel, OrderModel
from webapp.apps.orders.serializers import TelegramUserSerializer, ProductSerializer, OrderSerializer

ORDER_MESSAGE = """
<b>Заказ сформирован!</b>

Имя клиента: <i>{}</i>
Получатель: <i>@{}</i>
Заказ: <i>{}</i>

<b>Состав заказа:</b>
{}

В ближайшее время для подтверждения заказа с Вами свяжется менеджер @BagOnStore
"""

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

bot = None
if settings.BOT_TOKEN:
    bot = Bot(settings.BOT_TOKEN)


async def send_message(user_id: int, text: str):
    if not bot:
        return
    await bot.send_message(user_id, text, parse_mode=ParseMode.HTML)
    if settings.CHAT_ID:
        await bot.send_message(settings.CHAT_ID, text, parse_mode=ParseMode.HTML)
    await bot.session.close()


def create_order(user, products):
    tg_user, _ = TelegramUserModel.objects.get_or_create(
        user_id=user['user_id'],
        defaults={
            'username': user['username'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'phone_number': user['phone_number'],
        }
    )
    order = OrderModel.objects.create(tg_user=tg_user)
    for product in products:
        name = re.sub(r'<\/?[^>]*>', '', product['name'])
        price = re.sub(r'[^\d]*(\d+).*', '\g<1>', product['price'])
        obj = ProductModel.objects.create(
            name=name,
            price=price,
            amount=product['amount'],
        )
        order.products.add(obj)

    order.save()
    return order


class OrderList(APIView):

    def get(self, request):
        orders = OrderModel.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_serializer = TelegramUserSerializer(data=request.data.get('user', {}))
        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product_serializer = ProductSerializer(data=request.data.get('products', []), many=True)
        if not product_serializer.is_valid():
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_data = user_serializer.validated_data
        products_data = product_serializer.validated_data
        order = create_order(user_data, products_data)
        message = ORDER_MESSAGE.format(
            user_data['first_name'],
            user_data['username'],
            order.order_number,
            order,
        )
        async def run():
            await asyncio.gather(
                send_message(user_data['user_id'], message),
            )
        loop.run_until_complete(run())
        return Response(status=status.HTTP_201_CREATED)
