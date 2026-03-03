from django import forms
from .models import Product, Sales


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'supplier', 'sku', 'price', 'stock_level', 'threshold']


class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ['customer_name', 'product', 'quantity', 'status']

    def clean(self):
        """
        Cross-field validation to ensure the requested quantity 
        is actually available in the warehouse.
        """
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')
        
        if product and quantity and product.stock_level < quantity:
            raise forms.ValidationError(f"Not enough stock! Available: {product.stock_level}")
        return cleaned_data
