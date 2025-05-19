from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta

from .models import Proveedor, CuentaPorPagar, TipoDocumento, Pago
from .forms import ProveedorForm, CuentaPorPagarForm, PagoForm

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

# Listar cuentas por pagar
@login_required
def listar_cuentas(request):
    cuentas = CuentaPorPagar.objects.select_related('proveedor', 'tipo_documento').all()
    proveedores = Proveedor.objects.all()

    proveedor_id = request.GET.get('proveedor')
    fecha_desde = request.GET.get('desde')
    fecha_hasta = request.GET.get('hasta')

    if proveedor_id:
        cuentas = cuentas.filter(proveedor_id=proveedor_id)

    if fecha_desde:
        cuentas = cuentas.filter(fecha_emision__gte=fecha_desde)

    if fecha_hasta:
        cuentas = cuentas.filter(fecha_emision__lte=fecha_hasta)

    context = {
        'cuentas': cuentas,
        'proveedores': proveedores,
    }
    return render(request, 'core/cuentas/listar.html', context)


# Crear cuenta por pagar
@login_required
def crear_cuenta(request):
    if request.method == 'POST':
        form = CuentaPorPagarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuenta por pagar registrada")
            return redirect('listar_cuentas')
    else:
        form = CuentaPorPagarForm()
    return render(request, 'core/cuentas/formulario.html', {'form': form})

# Editar cuenta por pagar
@login_required
def editar_cuenta(request, pk):
    cuenta = get_object_or_404(CuentaPorPagar, pk=pk)
    form = CuentaPorPagarForm(request.POST or None, instance=cuenta)
    if form.is_valid():
        form.save()
        messages.success(request, "Cuenta por pagar actualizada")
        return redirect('listar_cuentas')
    return render(request, 'core/cuentas/formulario.html', {'form': form})

# Eliminar cuenta por pagar
@login_required
def eliminar_cuenta(request, pk):
    cuenta = get_object_or_404(CuentaPorPagar, pk=pk)
    cuenta.delete()
    messages.success(request, "Cuenta por pagar eliminada")
    return redirect('listar_cuentas')

# Listar pagos
@login_required
def listar_pagos(request):
    pagos = Pago.objects.select_related('cuenta__proveedor').all()
    return render(request, 'core/pagos/listar.html', {'pagos': pagos})

# Crear pago
@login_required
def crear_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pago registrado")
            return redirect('listar_pagos')
    else:
        form = PagoForm()
    return render(request, 'core/pagos/formulario.html', {'form': form})

# Eliminar pago
@login_required
def eliminar_pago(request, pk):
    pago = get_object_or_404(Pago, pk=pk)
    pago.delete()
    messages.success(request, "Pago eliminado")
    return redirect('listar_pagos')
