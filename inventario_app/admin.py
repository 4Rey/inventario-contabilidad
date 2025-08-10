# inventario_app/admin.py
from django.contrib import admin
from .models import TipoInventario, Almacen, Articulo, Transaccion

@admin.register(TipoInventario)
class TipoInventarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'descripcion', 'cuenta_contable', 'estado')
    list_editable = ('estado',)
    list_filter = ('estado',)

@admin.register(Almacen)
class AlmacenAdmin(admin.ModelAdmin):
    list_display = ('id', 'descripcion', 'ubicacion', 'estado')
    list_editable = ('estado',)
    list_filter = ('estado',)

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ('id', 'descripcion', 'tipo', 'stock', 'costo_unitario', 'estado')
    list_editable = ('stock', 'costo_unitario', 'estado')
    list_filter = ('tipo', 'estado')

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'tipo', 'articulo', 'almacen_origen', 'almacen_destino', 'fecha', 'cantidad', 'monto'
    )
    list_filter = ('tipo', 'fecha')
    readonly_fields = ('fecha',)

    fieldsets = (
        (None, {
            'fields': ('tipo', 'articulo', 'almacen_origen', 'almacen_destino')
        }),
        ('Detalles', {
            'fields': ('cantidad', 'monto', 'fecha')
        }),
    )
