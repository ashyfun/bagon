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


class OrderModel(TimeStampedModel):
    tg_user = models.ForeignKey(TelegramUserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    amount = models.PositiveSmallIntegerField(default=1)
