# inventario_app/views.py
from django.views.generic import (
    TemplateView, FormView, ListView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from django.contrib import messages
from django.conf import settings
from django import forms
import requests

from .models import TipoInventario, Articulo, Almacen, Transaccion
from .forms import (
    TipoInventarioForm,
    ArticuloForm,
    AlmacenForm,
    TransaccionForm
)



# ----- Home -----
class HomeView(TemplateView):
    template_name = 'inventario_app/home.html'


# ----- Mixin de protección de borrado -----
class ProtectedDeleteMixin:
    """
    Mixin para capturar errores de borrado protegido y eliminar por GET.
    """
    success_url = None
    delete_error_message = 'No se puede eliminar este registro porque tiene dependencias.'

    def get(self, request, *args, **kwargs):
        # Al llamar por GET, ejecuta delete directamente
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, 'Eliminación exitosa.')
            return response
        except ProtectedError:
            messages.error(request, self.delete_error_message)
            return redirect(self.success_url)


# ----- CRUD TipoInventario -----
class TipoInventarioList(ListView):
    model = TipoInventario
    template_name = 'inventario_app/tipo_list.html'
    context_object_name = 'tipos'


class TipoInventarioCreate(CreateView):
    model = TipoInventario
    form_class = TipoInventarioForm
    template_name = 'inventario_app/tipo_form.html'
    success_url = reverse_lazy('tipo_list')


class TipoInventarioUpdate(UpdateView):
    model = TipoInventario
    form_class = TipoInventarioForm
    template_name = 'inventario_app/tipo_form.html'
    success_url = reverse_lazy('tipo_list')


class TipoInventarioDelete(ProtectedDeleteMixin, DeleteView):
    model = TipoInventario
    success_url = reverse_lazy('tipo_list')
    delete_error_message = 'No se puede eliminar este tipo porque tiene artículos asociados.'


# ----- CRUD Artículo -----
class ArticuloList(ListView):
    model = Articulo
    template_name = 'inventario_app/articulo_list.html'
    context_object_name = 'articulos'


class ArticuloCreate(CreateView):
    model = Articulo
    form_class = ArticuloForm
    template_name = 'inventario_app/articulo_form.html'
    success_url = reverse_lazy('articulo_list')


class ArticuloUpdate(UpdateView):
    model = Articulo
    form_class = ArticuloForm
    template_name = 'inventario_app/articulo_form.html'
    success_url = reverse_lazy('articulo_list')


class ArticuloDelete(ProtectedDeleteMixin, DeleteView):
    model = Articulo
    success_url = reverse_lazy('articulo_list')
    delete_error_message = 'No se puede eliminar este artículo porque tiene transacciones asociadas.'


# ----- CRUD Almacén -----
class AlmacenList(ListView):
    model = Almacen
    template_name = 'inventario_app/almacen_list.html'
    context_object_name = 'almacenes'


class AlmacenCreate(CreateView):
    model = Almacen
    form_class = AlmacenForm
    template_name = 'inventario_app/almacen_form.html'
    success_url = reverse_lazy('almacen_list')


class AlmacenUpdate(UpdateView):
    model = Almacen
    form_class = AlmacenForm
    template_name = 'inventario_app/almacen_form.html'
    success_url = reverse_lazy('almacen_list')


class AlmacenDelete(ProtectedDeleteMixin, DeleteView):
    model = Almacen
    success_url = reverse_lazy('almacen_list')
    delete_error_message = 'No se puede eliminar este almacén porque tiene transacciones asociadas.'


# ----- CRUD Transacción -----
class TransaccionList(ListView):
    model = Transaccion
    template_name = 'inventario_app/transaccion_list.html'
    context_object_name = 'transacciones'


class TransaccionCreate(CreateView):
    model = Transaccion
    form_class = TransaccionForm
    template_name = 'inventario_app/transaccion_form.html'
    success_url = reverse_lazy('transaccion_list')


class TransaccionUpdate(UpdateView):
    model = Transaccion
    form_class = TransaccionForm
    template_name = 'inventario_app/transaccion_form.html'
    success_url = reverse_lazy('transaccion_list')


class TransaccionDelete(ProtectedDeleteMixin, DeleteView):
    model = Transaccion
    success_url = reverse_lazy('transaccion_list')
    delete_error_message = 'No se puede eliminar esta transacción.'


# ----- Reportes -----
class ExistenciaList(ListView):
    model = Articulo
    template_name = 'inventario_app/reporte_existencias.html'
    context_object_name = 'articulos'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(
                Q(descripcion__icontains=q) |
                Q(tipo__descripcion__icontains=q)
            )
        return qs


class MovimientoList(ListView):
    model = Transaccion
    template_name = 'inventario_app/reporte_movimientos.html'
    context_object_name = 'transacciones'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(
                Q(articulo__descripcion__icontains=q) |
                Q(tipo__icontains=q) |
                Q(almacen_origen__descripcion__icontains=q) |
                Q(almacen_destino__descripcion__icontains=q)
            )
        return qs


class KardexView(TemplateView):
    template_name = 'inventario_app/reporte_kardex.html'

    def get(self, request, articulo_id, *args, **kwargs):
        articulo = get_object_or_404(Articulo, pk=articulo_id)
        transs = Transaccion.objects.filter(articulo=articulo).order_by('fecha')
        saldo = 0
        movimientos = []
        for t in transs:
            if t.tipo == 'Entrada':
                saldo += t.cantidad
            elif t.tipo == 'Salida':
                saldo -= t.cantidad
            elif t.tipo == 'Ajuste':
                saldo = t.cantidad
            movimientos.append({'transaccion': t, 'saldo': saldo})
        return render(request, self.template_name, {
            'articulo': articulo,
            'movimientos': movimientos,
        })


# ----- Integración Contabilidad -----
from django import forms

class ContabilizarForm(forms.Form):
    fecha_desde = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha Desde'
    )
    fecha_hasta = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha Hasta'
    )

class ContabilizarView(FormView):
    template_name = 'inventario_app/contabilizar.html'
    form_class = ContabilizarForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault('transacciones', [])
        ctx.setdefault('total_monto', 0)
        ctx.setdefault('pendientes_count', 0)
        return ctx

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            return self.form_invalid(form)

        action = request.POST.get('action')  # 'consultar' | 'contabilizar'
        context = self.get_context_data(form=form)

        desde = form.cleaned_data['fecha_desde']
        hasta = form.cleaned_data['fecha_hasta']

        # Siempre consulta para mostrar tabla/totales
        qs = Transaccion.objects.filter(
            fecha__date__gte=desde,
            fecha__date__lte=hasta
        ).order_by('fecha')
        context['transacciones'] = qs
        context['total_monto'] = sum(t.monto for t in qs)

        pendientes = qs.filter(id_asiento__isnull=True)
        context['pendientes_count'] = pendientes.count()

        if action == 'consultar':
            return self.render_to_response(context)

        # Contabilizar real
        total_pendiente = float(sum(t.monto for t in pendientes))
        if total_pendiente <= 0:
            messages.warning(request, 'No hay transacciones pendientes para enviar.')
            return self.render_to_response(context)

        descripcion   = f'Asiento de Inventarios {desde} a {hasta}'
        fecha_asiento = hasta.isoformat()

        movimientos = [
            {'cuenta_Id': 6,  'tipoMovimiento': 'DB', 'montoAsiento': total_pendiente},  # Inventario
            {'cuenta_Id': 82, 'tipoMovimiento': 'CR', 'montoAsiento': total_pendiente},  # CxP Proveedor X
        ]

        ids_creados = []
        for mov in movimientos:
            body = {
                'descripcion':    descripcion,
                'fechaAsiento':   fecha_asiento,
                'cuenta_Id':      mov['cuenta_Id'],
                'tipoMovimiento': mov['tipoMovimiento'],  # 'DB' o 'CR'
                'montoAsiento':   mov['montoAsiento'],
                # 'auxiliar_Id': 4,  # Descomenta si el WS lo exige
            }
            try:
                resp = requests.post(
                    settings.CONTABILIDAD_API_URL,
                    headers={
                        'x-api-key': settings.CONTABILIDAD_API_KEY,
                        'Content-Type': 'application/json',
                    },
                    json=body,
                    timeout=15,
                )
            except requests.exceptions.RequestException as e:
                messages.error(request, f'Error de conexión con Contabilidad: {e}')
                return self.render_to_response(context)

            if resp.status_code not in (200, 201):
                messages.error(
                    request, f'Error {resp.status_code} en {mov["tipoMovimiento"]}: {resp.text[:200]}'
                )
                return self.render_to_response(context)

            try:
                data = resp.json()
            except Exception:
                data = {}

            curr_id = (data.get('data') or {}).get('id') \
                      or data.get('id') \
                      or data.get('idAsiento') \
                      or data.get('asiento_id')
            if curr_id is not None:
                ids_creados.append(str(curr_id))

        id_guardar = ",".join(ids_creados) if ids_creados else "ENVIADO"
        pendientes.update(id_asiento=id_guardar)
        messages.success(request, f'Enviado a Contabilidad. IDs: {id_guardar}')

        # refresca tabla
        qs = Transaccion.objects.filter(
            fecha__date__gte=desde,
            fecha__date__lte=hasta
        ).order_by('fecha')
        context['transacciones'] = qs
        context['total_monto'] = sum(t.monto for t in qs)
        context['pendientes_count'] = qs.filter(id_asiento__isnull=True).count()

        return self.render_to_response(context)
