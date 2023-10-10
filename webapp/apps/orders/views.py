import re
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

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
async def send_message(user_id: int, text: str):
    if not bot:
        return
    await bot.send_message(user_id, text, parse_mode=ParseMode.HTML)


async def write(data):
    print(data)


class OrderList(APIView):

    def get(self, request):
        return Response()

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        message = ORDER_MESSAGE.format(
            re.sub(r'(<br>|<\/?span[^>]*>)', '', validated_data['name']),
            validated_data['price'],
            validated_data['amount'],
        )
        async def run():
            await asyncio.gather(
                send_message(validated_data['user']['id'], message),
                write('Write data...'),
            )
        loop.run_until_complete(run())
        return Response(status=status.HTTP_201_CREATED)
