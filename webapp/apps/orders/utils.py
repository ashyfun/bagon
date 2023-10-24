from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode

from django.conf import settings

from webapp.apps.orders.models import TelegramUser, OrderItem, Order

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


async def send_group_message(text: str):
    if not (bot and settings.CHAT_ID):
        return
    await bot.send_message(settings.CHAT_ID, text, parse_mode=ParseMode.HTML)
    await bot.session.close()


def create_order(user: dict, items: list):
    tg_user, _ = TelegramUser.objects.update_or_create(
        user_id=user['user_id'],
        defaults={
            'username': user['username'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'phone_number': user['phone_number'],
        }
    )
    order = Order.objects.create(tg_user=tg_user)
    for item in items:
        obj = OrderItem.objects.create(**item)
        order.items.add(obj)

    order.save()
    return order


def get_order(user: dict):
    tg_user = TelegramUser.objects.get(user_id=user['user_id'])
    tg_user.phone_number = user['phone_number']
    tg_user.save()
    order = Order.objects.filter(tg_user=tg_user).last()
    return order
