from django.db import models

from authentication.models import User

# Create your models here.
class Bill(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    amount = models.IntegerField(default=0)
    service_fee = models.IntegerField(default=0)
    tax = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Billitem(models.Model):
    id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.IntegerField()
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)

class BillSplit(models.Model):
    id = models.AutoField(primary_key=True)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    billitem = models.ForeignKey(Billitem, on_delete=models.CASCADE)
    tax = models.IntegerField()
    service_fee = models.IntegerField()
    discount = models.IntegerField()
    amount = models.IntegerField()
    total_amount = models.IntegerField()
    paid = models.BooleanField(default=False)