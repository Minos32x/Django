from django.db import models

class Customer(models.Model):
    name=models.CharField(max_length=50)
    mobile=models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tickets(models.Model):
    customer_id=models.ForeignKey(Customer,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    notes=models.TextField()

    # return customer name instead of id
    def __str__(self):
        return self.customer_id

    def __str__(self):
        return self.notes
