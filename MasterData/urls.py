from django.urls import path
from . import views


urlpatterns = [
 path('fetch_cat/', views.fetch_cat, name="fetch_cat"), 
 path('fetch_p_cat/', views.fetch_p_cat, name="fetch_p_cat"), 

 path('edit_cat/', views.edit_cat, name="edit_cat"), 
 path('add_cat/', views.add_cat, name="add_cat"), 
 path('delete_cat/', views.delete_cat, name="delete_cat"), 
 path('fetch_uom/', views.fetch_uom, name="fetch_uom"), 
 path('add_product/', views.add_product, name="add_product"),
 path('fetch_products/', views.fetch_products, name="fetch_products"),
 path ('fetch_a_product/', views.fetch_a_product, name="fetch_a_product"),
 path ('edit_mat/', views.edit_mat, name="edit_mat"),
 path ('delete_mat/', views.delete_mat, name="delete_mat"),
 path ('add_product_Img/', views.add_product_Img, name="add_product_Img"),
 path ('add_UOM/', views.add_UOM, name="add_UOM"),
 path ('edit_UOM/', views.edit_UOM, name="edit_UOM"),
 path ('delete_uom/', views.delete_uom, name="delete_uom"),
 path ('edit_settings/', views.edit_settings, name="edit_settings"),
 path ('fetch_settings/', views.fetch_settings, name="fetch_settings"),
 path ('fetch_discounts/', views.fetch_discounts, name="fetch_discounts"),
 path ('add_discount/', views.add_discount, name="add_discount"),
 path ('fetch_disc_types/', views.fetch_disc_types, name="fetch_disc_types"),
 path ('fetch_a_product_uom/', views.fetch_a_product_uom, name="fetch_a_product_uom"),
 path ('fetch_a_discount/', views.fetch_a_discount, name="fetch_a_discount"),
 path ('edit_discount/', views.edit_discount, name="edit_discount"),
 path ('delete_discount/', views.delete_discount, name="delete_discount"),
 path ('fetch_sub_cat/', views.fetch_sub_cat, name="fetch_sub_cat"),
 path ('add_bonusbuy/', views.add_bonusbuy, name="add_bonusbuy"),
 path ('fetch_bonusBuy/', views.fetch_bonusBuy, name="fetch_bonusBuy"),
 path ('fetch_a_bonusbuy/', views.fetch_a_bonusbuy, name="fetch_a_bonusbuy"),
 path ('edit_bonusBuy/', views.edit_bonusBuy, name="edit_bonusBuy"),


   ]