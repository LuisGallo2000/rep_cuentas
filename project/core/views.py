from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Proveedor
from .forms import ProveedorForm

# Página de inicio
def home(request):
    return render(request, 'core/home.html')

# Login de usuario
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Sesión iniciada correctamente")
            return redirect('home')
        else:
            messages.error(request, "Credenciales incorrectas")
            return redirect('login')
    return render(request, 'core/login.html')

# Logout
def logout_user(request):
    logout(request)
    messages.success(request, "Sesión cerrada")
    return redirect('home')

# Listado de proveedores
@login_required
def listar_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'core/proveedores/listar.html', {'proveedores': proveedores})

# Crear proveedor
@login_required
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor registrado")
            return redirect('listar_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'core/proveedores/formulario.html', {'form': form})

# Editar proveedor
@login_required
def editar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    form = ProveedorForm(request.POST or None, instance=proveedor)
    if form.is_valid():
        form.save()
        messages.success(request, "Proveedor actualizado")
        return redirect('listar_proveedores')
    return render(request, 'core/proveedores/formulario.html', {'form': form})

# Eliminar proveedor
@login_required
def eliminar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    proveedor.delete()
    messages.success(request, "Proveedor eliminado")
    return redirect('listar_proveedores')
