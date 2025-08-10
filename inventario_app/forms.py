from django import forms
from django.core.exceptions import ValidationError
from .models import TipoInventario, Articulo, Almacen, Transaccion

class TipoInventarioForm(forms.ModelForm):
    class Meta:
        model = TipoInventario
        fields = ['descripcion', 'cuenta_contable', 'estado']
        widgets = {
            'descripcion':     forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Descripción',
                'required': True
            }),
            'cuenta_contable': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Cuenta contable',
                'required': True
            }),
            'estado':          forms.CheckboxInput(attrs={
                'class':'form-check-input'
            }),
        }

    def clean_descripcion(self):
        desc = self.cleaned_data['descripcion']
        if TipoInventario.objects.filter(descripcion__iexact=desc).exists():
            raise ValidationError("Ya existe un tipo con esa descripción.")
        return desc

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['descripcion','tipo','stock','costo_unitario','estado']
        widgets = {
            'descripcion':    forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Descripción',
                'required': True
            }),
            'tipo':           forms.Select(attrs={
                'class':'form-select',
                'required': True
            }),
            'stock':          forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder':'Stock inicial',
                'min': 0,
                'required': True
            }),
            'costo_unitario': forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder':'Costo unitario',
                'min': 0,
                'step':'0.01',
                'required': True
            }),
            'estado':         forms.CheckboxInput(attrs={
                'class':'form-check-input'
            }),
        }

    def clean_stock(self):
        stock = self.cleaned_data['stock']
        if stock < 0:
            raise ValidationError("El stock no puede ser negativo.")
        return stock

    def clean_costo_unitario(self):
        costo = self.cleaned_data['costo_unitario']
        if costo < 0:
            raise ValidationError("El costo unitario no puede ser negativo.")
        return costo

class AlmacenForm(forms.ModelForm):
    class Meta:
        model = Almacen
        fields = ['descripcion','ubicacion','estado']
        widgets = {
            'descripcion': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Descripción',
                'required': True
            }),
            'ubicacion':   forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Ubicación',
                'required': True
            }),
            'estado':      forms.CheckboxInput(attrs={
                'class':'form-check-input'
            }),
        }

    def clean_descripcion(self):
        desc = self.cleaned_data['descripcion']
        if Almacen.objects.filter(descripcion__iexact=desc).exists():
            raise ValidationError("Ya existe un almacén con esa descripción.")
        return desc

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['tipo','articulo','almacen_origen','almacen_destino','cantidad','monto']
        widgets = {
            'tipo':            forms.Select(attrs={
                'class':'form-select',
                'required': True
            }),
            'articulo':        forms.Select(attrs={
                'class':'form-select',
                'required': True
            }),
            'almacen_origen':  forms.Select(attrs={
                'class':'form-select'
            }),
            'almacen_destino': forms.Select(attrs={
                'class':'form-select'
            }),
            'cantidad':        forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder':'Cantidad',
                'min': 1,
                'required': True
            }),
            'monto':           forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder':'Monto',
                'min': 0.01,
                'step':'0.01',
                'required': True
            }),
        }

    def clean(self):
        cleaned = super().clean()
        tipo = cleaned.get('tipo')
        cantidad = cleaned.get('cantidad')
        articulo = cleaned.get('articulo')
        origen = cleaned.get('almacen_origen')
        destino = cleaned.get('almacen_destino')

        if tipo == 'Salida' and articulo and cantidad:
            if cantidad > articulo.stock:
                self.add_error('cantidad',
                    f"Stock insuficiente (disponible: {articulo.stock})."
                )
        if tipo == 'Traslado':
            if not origen or not destino:
                raise ValidationError("Debe seleccionar origen y destino para Traslado.")
            if origen == destino:
                raise ValidationError("Origen y destino no pueden ser el mismo.")
        return cleaned