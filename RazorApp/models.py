from django.db import models


# Create your models here.
class Coffee(models.Model):
    name = models.CharField(max_length=100, default='Rahul Kumar')
    email = models.EmailField(default='rahulkumar123@example.com')
    contact = models.IntegerField(default='9999999999')
    address = models.TextField(default="House no 215 Saharanpur Uttar Pradesh India 247001")
    amount = models.IntegerField(default=0)
    order_id = models.CharField(max_length=200, default='')
    payment_id = models.CharField(max_length=200, default='')
    signature_id = models.CharField(max_length=200, default='')
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name
