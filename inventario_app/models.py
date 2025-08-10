from django.db import models
from django.core.validators import MinValueValidator

class TipoInventario(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    cuenta_contable = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion


class Articulo(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoInventario, on_delete=models.PROTECT)
    stock = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    costo_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion


class Almacen(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

class Transaccion(models.Model):
    id = models.AutoField(primary_key=True)
    TIPO_CHOICES = [
        ('Entrada', 'Entrada'),
        ('Salida', 'Salida'),
        ('Traslado', 'Traslado'),
        ('Ajuste', 'Ajuste'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    articulo = models.ForeignKey(Articulo, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    monto = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    almacen_origen = models.ForeignKey(
        Almacen,
        related_name='salidas',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    almacen_destino = models.ForeignKey(
        Almacen,
        related_name='entradas',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    # 1. Campo nuevo para guardar el ID que devuelve Contabilidad
    id_asiento = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='ID Asiento Contable'
    )

    def __str__(self):
        return f'{self.tipo} #{self.id}'