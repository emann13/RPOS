from django.urls import path
from . import views


urlpatterns = [
 path('fetch_cat/', views.fetch_cat, name="fetch_cat"), 
 path('edit_cat/', views.edit_cat, name="edit_cat"), 
 path('add_cat/', views.add_cat, name="add_cat"), 
 path('delete_cat/', views.delete_cat, name="delete_cat"), 
 path('fetch_uom/', views.fetch_uom, name="fetch_uom"), 
 path('add_product/', views.add_product, name="add_product"),
 path('fetch_products/', views.fetch_products, name="fetch_products"),
 path ('fetch_a_product/', views.fetch_a_product, name="fetch_a_product"),
 path ('edit_mat/', views.edit_mat, name="edit_mat")

   ]