# from django.core.mail import send_mail
# from django.db.models import F
# from .models import Product, PurchaseOrder


# def send_low_stock_alerts():
#     low_stock_items = Product.objects.filter(stock_level__lte=F('threshold'))
#     if low_stock_items.exists():
#         message = "The following items are low on stock:\n\n"
#         for item in low_stock_items:
#             message += f"{item.name}: {item.stock_level} remaining  (Threshold: {item.threshold})\n"

#         send_mail(
#             'Low Stock Alert!',
#             message,
#             'system@inventory.com',
#             ['nareshbaskar11@gmail.com'],
#             fail_silently=False,
#         )

