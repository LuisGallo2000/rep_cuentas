from django.db import models
from project.choices import EstadoEntidades, EstadoCuenta
import uuid
from django.core.exceptions import ValidationError
from django.db import transaction

class TipoDocumento(models.Model):
    tipo_documento_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'tipos_documento'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    proveedor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150)
    ruc = models.CharField(max_length=11, unique=True)
    direccion = models.CharField(max_length=255, null=True)
    correo = models.EmailField(max_length=255, null=True)
    telefono = models.CharField(max_length=15, null=True)
    estado = models.IntegerField(choices=EstadoEntidades.choices, default=EstadoEntidades.ACTIVO)

    class Meta:
        db_table = 'proveedores'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class CuentaPorPagar(models.Model):
    cuenta_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.RESTRICT, db_column='proveedor_id')
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.RESTRICT)
    nro_documento = models.CharField(max_length=20)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    monto_total = models.DecimalField(max_digits=12, decimal_places=2)
    saldo_pendiente = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.IntegerField(choices=EstadoCuenta.choices, default=EstadoCuenta.ACTIVA)

    class Meta:
        db_table = 'cuentas_por_pagar'
        ordering = ['fecha_vencimiento']

    def __str__(self):
        return f'{self.nro_documento} - {self.proveedor.nombre}'

class Pago(models.Model):
    pago_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cuenta = models.ForeignKey(CuentaPorPagar, on_delete=models.CASCADE, related_name='pagos', db_column='cuenta_id')
    fecha_pago = models.DateField()
    monto_pagado = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'pagos'
        ordering = ['fecha_pago']

    def __str__(self):
        return f'Pago {self.monto_pagado} - {self.fecha_pago}'

    def clean(self):
        if self.monto_pagado <= 0:
            raise ValidationError("El monto pagado debe ser mayor a cero.")
        if self.pk is None:
            if self.monto_pagado > self.cuenta.saldo_pendiente:
                raise ValidationError("El monto pagado no puede exceder el saldo pendiente.")

    def save(self, *args, **kwargs):
        self.clean()
        with transaction.atomic():
            cuenta = self.cuenta
            nuevo_saldo = cuenta.saldo_pendiente - self.monto_pagado
            if nuevo_saldo < 0:
                raise ValidationError("El pago excede el saldo pendiente.")
            cuenta.saldo_pendiente = nuevo_saldo
            if nuevo_saldo == 0:
                from project.choices import EstadoCuenta
                cuenta.estado = EstadoCuenta.CANCELADA
            cuenta.save()
            super().save(*args, **kwargs)