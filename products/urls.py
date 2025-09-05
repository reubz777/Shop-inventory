from django.urls import path, include
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.BatchList.as_view(), name = 'product-list'),
    path('create-batch/', views.CreateBatch.as_view(), name='create-batch'),
    path('delete-batch/<int:pk>/', views.DeleteBatch.as_view(), name='delete-batch'),
    path('consolidation-batch/<int:pk>/', views.ConsolidationBatch.as_view(), name='consolidation-batch'),
]