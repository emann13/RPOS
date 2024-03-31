from django.urls import path
from . import views


urlpatterns = [
path('fetch_orders/', views.fetch_orders, name="fetch_orders"),
path('fetch_order_items/', views.fetch_order_items, name="fetch_order_items"),
path('assign_order/', views.assign_order, name="assign_order"),
path('cancel_order/', views.cancel_order, name="cancel_order"),
path('change_stat/', views.change_stat, name="change_stat"),

]
