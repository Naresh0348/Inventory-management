from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/add/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/edit/<int:pk>/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('suppliers/', views.SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/add/', views.SupplierCreateView.as_view(), name='supplier_add'),
    path('purchase-orders/', views.POListView.as_view(), name='po_list'),
    path('purchase-order/add/', views.POCreateView.as_view(), name='po_add'),
    path('sales/', views.SalesListView.as_view(), name='sales_list'),
    path('sales/add/', views.SalesCreateView.as_view(), name='sales_add'),
    path('report/inventory/', views.InventoryReportView.as_view(), name='inventory_report'),
    path('report/sales/', views.SalesReportView.as_view(), name='sales_report'),
    path('report/expenditure/', views.PurchaseReportView.as_view(), name='purchase_report'),
    path('notification/', views.NotificationView.as_view(), name="notification"),
]