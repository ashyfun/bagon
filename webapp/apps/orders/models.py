from webapp.apps.base import models as base_models
from webapp.apps.base.models import models
from webapp.apps.orders import messages


class TelegramUser(base_models.TimeStampedModel):
    user_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=32, null=True, blank=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)


class OrderItem(base_models.TimeStampedModel):

    class Size(models.TextChoices):
        S = 'S'
        S_PLUS = 'S+'
        M = 'M'
        M_PLUS = 'M+'
        L = 'L'
        L_PLUS = 'L+'

    name = models.CharField(max_length=128)
    size = models.CharField(max_length=2, choices=Size.choices, default=Size.S)
    color = models.CharField(max_length=32)
    price = models.PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return messages.ORDER_ITEM_MESSAGE.format(
            self.name,
            self.color,
            self.size,
            self.quantity,
            self.price,
        )


class Order(base_models.TimeStampedModel):
    tg_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)

    @property
    def order_number(self):
        quantity = str(self.items.count())
        leading_zeros = (4 - len(quantity)) * '0'
        return self.created_at.strftime('%d%m%H%M') + '-' + str(self.id) + '-' + leading_zeros + quantity

    def __str__(self):
        total_cost, text = 0, ''
        for item in self.items.all():
            total_cost += item.quantity * item.price
            text += f'{item}'
        return f'{text}\n<b>Стоимость</b>: <i>{total_cost} RUB</i>'
