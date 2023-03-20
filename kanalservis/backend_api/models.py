from django.db import models

# Create your models here.
class kanalservis(models.Model):
    number = models.IntegerField(unique=True, blank=False, db_column='№')
    order = models.IntegerField(unique=True, blank=False, db_column='заказ№')
    price_usd = models.IntegerField(blank=False, db_column='стоимость$')
    price_rub = models.IntegerField(blank=False, db_column='стоимостьРуб')
    ord_date = models.DateField(blank=False, db_column='срок_поставки')