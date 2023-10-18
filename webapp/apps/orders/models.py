from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TelegramUserModel(TimeStampedModel):
    user_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=32, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    phone_number = models.CharField(max_length=15)


class ProductModel(TimeStampedModel):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    amount = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'Товар: {self.name}\nЦена: {self.price} RUB / шт.\nВ количестве: {self.amount}'


class OrderModel(TimeStampedModel):
    tg_user = models.ForeignKey(TelegramUserModel, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductModel)

    @property
    def order_number(self):
        amount = str(self.products.count())
        leading_zeros = (4 - len(amount)) * '0'
        return self.created_at.strftime('%d%m%H%M') + '-' + str(self.id) + '-' + leading_zeros + amount

    def __str__(self):
        total_cost = 0
        text = ''
        for item in self.products.all():
            total_cost += item.amount * item.price
            text += f'\n{item}\n'
        return f'{text}\n<b>Стоимость</b>: <i>{total_cost} RUB</i>'
