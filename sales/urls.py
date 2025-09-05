from django.urls import path, include
from . import views

app_name = 'sales'

urlpatterns = [
    path('',views.SaleListView.as_view(), name='sales-list'),
    path('select2/', include('django_select2.urls')),
    path('create-sale/', views.CreateSaleView.as_view(), name='sale-create'),
    path('delete-sale/<int:product_id>/', views.CreateSaleView.as_view(), name='sale-create'),

]