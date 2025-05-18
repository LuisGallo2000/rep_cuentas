from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Proveedores
    path('proveedores/', views.listar_proveedores, name='listar_proveedores'),
    path('proveedores/nuevo/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedores/editar/<uuid:pk>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<uuid:pk>/', views.eliminar_proveedor, name='eliminar_proveedor'),
]