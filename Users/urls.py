from django.urls import path
from . import views


urlpatterns = [
 path('login/', views.login, name="login"),   
 path('fetch_admins/', views.fetch_admins, name ="fetch_admins"),
 path('add_admin/', views.add_admin, name ="add_admin"),
 path('edit_admin/', views.edit_admin, name="edit_admin"),
 path('delete_admin/', views.delete_admin, name="delete_admin"),
 path('reset_pass_admin/', views.reset_pass_admin, name="reset_pass_admin"),
 path('fetch_permissions/', views.fetch_permissions, name ="fetch_permissions"),
 path('fetch_Roles/', views.fetch_Roles, name ="fetch_Roles"),
 path('fetch_Auths/', views.fetch_Auths, name ="fetch_Auths"),
 path('add_role/', views.add_role, name ="add_role"),
 path('fetch_R_Auths/',views.fetch_R_Auths, name="fetch_R_Auths"),
 path('edit_role/',views.edit_role, name="edit_role"),
 path('delete_role/',views.delete_role, name="delete_role"),
 path('add_user/', views.add_user, name ="add_user"),
 path('fetch_users/', views.fetch_users, name ="fetch_users"),
 path('edit_user/', views.edit_user, name ="edit_user"),
 path('delete_user/', views.delete_user, name ="delete_user"),
 path('count_active_users/', views.count_active_users, name ="count_active_users"),
 path('get_License/', views.get_License, name ="get_License"),
 path('edit_license/', views.edit_license, name ="edit_license"),
 path('get_ecs_admin/' , views.get_ecs_admin, name ="get_ecs_admin"),
 path('fetch_users_p/' , views.fetch_users_p, name ="fetch_users_p"),
 path('fetch_a_role_Auths/',views.fetch_a_role_Auths, name="fetch_a_role_Auths"),
 path('fetch_an_admin_Auths/',views.fetch_an_admin_Auths, name="fetch_an_admin_Auths"),
 path('fetch_drivers/' , views.fetch_drivers, name ="fetch_drivers"),
 path('add_driver/', views.add_driver, name ="add_driver"),
 path('edit_driver/', views.edit_driver, name ="edit_driver"),
 path('delete_driver/', views.delete_driver, name ="delete_driver"),
 path('fetch_customers/', views.fetch_customers, name ="fetch_customers"),
 path('export_users_to_excel/', views.export_users_to_excel, name ="export_users_to_excel"),
 path('fetch_user_addresses/', views.fetch_user_addresses, name ="fetch_user_addresses"),


]
