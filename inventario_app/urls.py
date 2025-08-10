from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.HomeView.as_view(), name='home'),

    # CRUD Tipos de Inventario
    path('tipos/', views.TipoInventarioList.as_view(), name='tipo_list'),
    path('tipos/nuevo/', views.TipoInventarioCreate.as_view(), name='tipo_create'),
    path('tipos/<int:pk>/editar/', views.TipoInventarioUpdate.as_view(), name='tipo_update'),
    path('tipos/<int:pk>/eliminar/', views.TipoInventarioDelete.as_view(), name='tipo_delete'),

    # CRUD Artículos
    path('articulos/', views.ArticuloList.as_view(), name='articulo_list'),
    path('articulos/nuevo/', views.ArticuloCreate.as_view(), name='articulo_create'),
    path('articulos/<int:pk>/editar/', views.ArticuloUpdate.as_view(), name='articulo_update'),
    path('articulos/<int:pk>/eliminar/', views.ArticuloDelete.as_view(), name='articulo_delete'),

    # CRUD Almacenes
    path('almacenes/', views.AlmacenList.as_view(), name='almacen_list'),
    path('almacenes/nuevo/', views.AlmacenCreate.as_view(), name='almacen_create'),
    path('almacenes/<int:pk>/editar/', views.AlmacenUpdate.as_view(), name='almacen_update'),
    path('almacenes/<int:pk>/eliminar/', views.AlmacenDelete.as_view(), name='almacen_delete'),

    # CRUD Transacciones
    path('transacciones/', views.TransaccionList.as_view(), name='transaccion_list'),
    path('transacciones/nuevo/', views.TransaccionCreate.as_view(), name='transaccion_create'),
    path('transacciones/<int:pk>/editar/', views.TransaccionUpdate.as_view(), name='transaccion_update'),
    path('transacciones/<int:pk>/eliminar/', views.TransaccionDelete.as_view(), name='transaccion_delete'),

    # Reportes
    path('reportes/existencias/', views.ExistenciaList.as_view(), name='reporte_existencias'),
    path('reportes/movimientos/', views.MovimientoList.as_view(), name='reporte_movimientos'),
    path('reportes/kardex/<int:articulo_id>/', views.KardexView.as_view(), name='reporte_kardex'),

 # Pantalla de Envío a Contabilidad
    path('contabilizar/', views.ContabilizarView.as_view(), name='contabilizar'),
]