from django.db import models # type: ignore
from django.utils import timezone # type: ignore
from datetime import date



class stockx(models.Model):
    item_name = models.CharField(max_length=50, null=True, blank=True)
    stock_source = models.CharField(max_length=50, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=15.00, null=True, blank=True) 
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=10.00, null=False, blank=True)
    stock_branch = models.CharField(max_length=50, null=True, blank=True)
    total_quantity = models.IntegerField(default=0, null=True, blank=True)
    issued_quantity = models.IntegerField(default=0, null=False, blank=True)

    

    def __str__(self):
        return self.item_name


class Sale(models.Model):
    item = models.ForeignKey(stockx, on_delete=models.CASCADE)
    quantity = models.IntegerField( null=False, blank=True)
    amount_received = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=True)
    issued_to = models.CharField(max_length=50, null=True, blank=True)
    unitcost = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        return self.quantity * self.item.total_price

    def get_change(self):
        return self.amount_received - self.get_total()
        
    
class Product(models.Model):
    item_name = models.CharField(max_length=255, null=True)
    total_quantity = models.PositiveIntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.item_name
    

class CreditSale(models.Model):
    buyer_name = models.CharField(max_length=100 )
    branch = models.CharField(max_length=14, null = True)
    location = models.CharField(max_length=100, null = True)
    contact = models.CharField(max_length=15, null = True)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sales_agent_name = models.CharField(max_length=100 )
    due_date = models.DateField(auto_now_add=True)
    product_name = models.CharField(max_length=100, null = True)
    tonnage = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_dispatch = models.DateField()

    def __str__(self):
        return f"Sale by {self.buyer_name} on {self.date_of_dispatch}"
    


