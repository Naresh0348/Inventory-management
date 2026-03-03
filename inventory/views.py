from django.shortcuts import render, redirect
from django.db import models
from django.db.models import Sum, F
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse_lazy
from .forms import ProductForm, SalesForm
from .models import Product, Sales, Supplier, PurchaseOrder
from django.contrib import messages
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, TemplateView
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


@login_required(login_url='login')
@never_cache # preventing the login info to store in users browser
def dashboard_view(request):
    context = {
        'total_products': Product.objects.all().count(),
        'low_stock_count': Product.objects.filter(stock_level__lte=models.F('threshold')).count(),
        'pending_orders': Sales.objects.filter(status='PENDING').count(),
        'total_suppliers': Supplier.objects.all().count(),
        'recent_sales': Sales.objects.order_by("-sale_date")[:5],
    }

    return render(request, "inventory/index.html", context)


@permission_required('inventory.add_product', raise_exception=True)
def add_product(request):
    return render(request, 'inventory/product_form.html')


def register_view(request):
    """
    Handles user registration and automatically asigns 
    new user to Staff group.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            staff_group, created = Group.objects.get_or_create(name='staff')
            user.groups.add(staff_group)

            messages.success(request, f'Account created for {user.username}! You are now a staff member.')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'inventory/register.html', {'form': form})


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'inventory.add_product'


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'inventory.change_product'


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'inventory/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'inventory.delete_product'


class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'inventory/supplier_list.html'
    context_object_name = 'suppliers'


class SupplierCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Supplier
    fields = ['company_name', 'contact_person', 'email', 'phone']
    template_name = 'inventory/supplier_form.html'
    success_url = reverse_lazy('supplier_list')
    permission_required = 'inventory.add_supplier'


class POListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = PurchaseOrder
    template_name = 'inventory/po_list.html'
    context_object_name = 'orders'
    ordering = ['-order_date']
    permission_required = 'inventory.view_purchaseorder'


class POCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = PurchaseOrder
    fields = ['product', 'supplier', 'quantity', 'status']
    template_name = 'inventory/po_form.html'
    success_url = reverse_lazy('dashboard')
    permission_required = 'inventory.add_purchaseorder'


class SalesListView(LoginRequiredMixin, ListView):
    model = Sales
    template_name = 'inventory/sales_list.html'
    context_object_name = 'sales'
    ordering = ['-sale_date']


class SalesCreateView(LoginRequiredMixin, CreateView):
    model = Sales
    form_class = SalesForm
    template_name = 'inventory/sales_form.html'
    success_url = reverse_lazy('sales_list')
    permission_required = 'inventory.add_sales'


class InventoryReportView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/inventory_report.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # calculating the total value of our products in the inventory
        context['total_value'] = Product.objects.aggregate(
            total=Sum(F('price') * F('stock_level'))
        )['total'] or 0

        # number of products below threshold
        context['shortage_count'] = Product.objects.filter(stock_level__lte=F('threshold')).count()

        return context
    

class SalesReportView(LoginRequiredMixin, ListView):
    model = Sales
    template_name = 'inventory/sales_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        # calculating the total revenue 
        def get_revenue(days):
            start_date = now - timedelta(days=days)
            return Sales.objects.filter(sale_date__gte=start_date).aggregate(
                total=Sum(F('quantity') * F('product__price'))
            )['total'] or 0
        
        # revenue calculation (daily, weekly, monthly, average daily revenue)
        weekly_rev = get_revenue(7)
        context['daily_revenue'] = get_revenue(1)
        context['weekly_revenue'] = weekly_rev
        context['monthly_revenue'] = get_revenue(30)
        context['avg_daily_rev'] = weekly_rev / 7

        return context
    

class PurchaseReportView(LoginRequiredMixin, ListView):
    model = PurchaseOrder
    template_name = 'inventory/purchase_report.html'
    context_object_name = 'orders'

    # total amount spent on purchasing products
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_spent'] = PurchaseOrder.objects.filter(status='RECEIVED').aggregate(
            total=Sum(F('quantity') * F('product__price'))
        )['total'] or 0

        return context

    
class NotificationView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/notification.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Low stock 
        context['low_stock'] = Product.objects.filter(stock_level__lte=F('threshold'))

        # Pending Supplier Orders
        three_days_ago = timezone.now() - timedelta(days=1)
        context['overdue_orders'] = PurchaseOrder.objects.filter(
            status='PENDING',
            order_date__lte=three_days_ago,
        )

        # High Demand Products
        context['high_demand'] = Product.objects.annotate(
            total_sold=Sum('sales__quantity')
        ).filter(total_sold__gte=20)

        return context

