from django.db import models
from django.db.models import F
from django.core.exceptions import ValidationError


class Category(models.Model):
    """Groups products (Eg. Stationary, Electronics)"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    
class Supplier(models.Model):
    """Vendors who provide the products."""
    company_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.company_name} ({self.contact_person})"
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    sku = models.CharField(max_length=50, unique=True) # stock keeping units (unique code for products)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_level = models.PositiveIntegerField(default=0)
    threshold = models.PositiveIntegerField(default=10)  

    @property
    def is_low_stock(self):
        # Returns true if product falls to or below threshold.
        return self.stock_level <= self.threshold
    
    def __str__(self):
        return f"{self.name} ({self.sku})"
    
    
class Sales(models.Model):
    """Records outgoing stock. Decrements Product stock_level upon creation."""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('COMPLETED', 'Completed'),

    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    customer_name = models.CharField(max_length=200)
    sale_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def save(self, *args, **kwargs):
        # Only subtract stock_level if this is a new sale.
        if self.pk is None:
            if self.product.stock_level < self.quantity:
                raise ValidationError(f"Not enought stock!  Available: {self.product.stock_level}")
            
            self.product.stock_level = F('stock_level') - self.quantity
            self.product.save()

        super().save(*args, **kwargs)


class PurchaseOrder(models.Model):
    """Records incoming stock. Increments Product stock_level when status hits 'RECEIVED'."""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RECEIVED', 'Received'),
        ('CANCELLED', 'Cancelled'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def save(self, *args, **kwargs):
        if self.pk:
            # check the version currently in the DB to see if the status just changed
            old_status = PurchaseOrder.objects.get(pk=self.pk).status
            if old_status != 'RECEIVED' and self.status == 'RECEIVED':
                self.product.stock_level += self.quantity
                self.product.save()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ordered-{self.quantity} for {self.product.name} from {self.supplier}"
