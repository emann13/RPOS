from django.urls import path
from . import views


urlpatterns = [
 path('add_store/', views.add_store, name="add_store"),   
 path('fetch_stores/', views.fetch_stores, name="fetch_stores"),   
 path('delete_store/', views.delete_store, name="delete_store"),   
 path('edit_store/', views.edit_store, name="edit_store"),   
 path('fetch_regions', views.fetch_regions, name="fetch_regions"),
 
]
