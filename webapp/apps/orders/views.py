import re
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from webapp.apps.orders.models import TelegramUserModel, OrderModel
from webapp.apps.orders.serializers import OrderSerializer

ORDER_MESSAGE = """
Товар: <i>{}</i>
Стоимость: <b>{}</b>
Количество: <b>{}</b>
"""

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

bot, dp = None, Dispatcher()
if settings.BOT_TOKEN:
    bot = Bot(settings.BOT_TOKEN)


@dp.message()
async def send_message(user_id: int, username: str, text: str):
    if not bot:
        return
    await bot.send_message(user_id, text, parse_mode=ParseMode.HTML)
    if settings.CHAT_ID:
        await bot.send_message(settings.CHAT_ID, f'@{username}{text}', parse_mode=ParseMode.HTML)


def save_to_db(data):
    data_tg_user = data['tg_user']
    tg_user, _ = TelegramUserModel.objects.get_or_create(
        user_id=data_tg_user['user_id'],
        defaults={
            'username': data_tg_user['username'],
            'first_name': data_tg_user['first_name'],
            'last_name': data_tg_user['last_name'],
        }
    )
    price = re.sub(r'[^\d]*(\d+).*', '\g<1>', data['price'])
    OrderModel.objects.create(
        tg_user=tg_user,
        name=data['name'],
        price=price
    )


class OrderList(APIView):

    def get(self, request):
        orders = OrderModel.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        validated_data['name'] = re.sub(r'(<br>|<\/?span[^>]*>)', '', validated_data['name'])
        message = ORDER_MESSAGE.format(
            validated_data['name'],
            validated_data['price'],
            validated_data['amount'],
        )
        save_to_db(validated_data),
        async def run():
            await asyncio.gather(
                send_message(validated_data['tg_user']['user_id'], validated_data['tg_user']['username'], message),
            )
        loop.run_until_complete(run())
        return Response(status=status.HTTP_201_CREATED)
