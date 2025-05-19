from django import forms
from .models import Proveedor, CuentaPorPagar, TipoDocumento, Pago

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'ruc', 'direccion', 'correo', 'telefono', 'estado']

class CuentaPorPagarForm(forms.ModelForm):
    class Meta:
        model = CuentaPorPagar
        fields = '__all__'
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['cuenta', 'fecha_pago', 'monto_pagado']
        widgets = {
            'fecha_pago': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        cuenta = cleaned_data.get("cuenta")
        monto = cleaned_data.get("monto_pagado")

        if monto is not None and monto <= 0:
            raise forms.ValidationError("El monto pagado debe ser mayor a cero.")

        if cuenta and monto and monto > cuenta.saldo_pendiente:
            raise forms.ValidationError("El monto no puede exceder el saldo pendiente.")