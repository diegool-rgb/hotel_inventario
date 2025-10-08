from django import forms
from django.core.validators import MinValueValidator
from decimal import Decimal
from .models import Producto, Categoria, Area, Proveedor, EntradaStock, DetalleEntradaStock


class AgregarProductoForm(forms.ModelForm):
    """Formulario para agregar un nuevo producto con stock inicial"""
    
    # Campos adicionales para la primera compra
    area_inicial = forms.ModelChoiceField(
        queryset=Area.objects.filter(activo=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Área donde se guardará",
        help_text="Selecciona el área donde se almacenará inicialmente el producto",
        required=False,
        empty_label="-- Seleccionar área (opcional) --"
    )
    
    cantidad_inicial = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0.01',
            'step': '0.01',
            'placeholder': '0.00'
        }),
        label="Cantidad inicial",
        help_text="Cantidad comprada en esta primera compra",
        required=False
    )
    
    numero_factura = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de factura o boleta'
        }),
        label="Número de Factura/Boleta",
        help_text="Número del comprobante de compra",
        required=False
    )
    
    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.filter(activo=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Proveedor",
        help_text="Proveedor de donde se compró el producto",
        required=False,
        empty_label="-- Seleccionar proveedor --"
    )
    
    comprobante = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        label="Foto de Boleta/Factura",
        help_text="Sube una foto del comprobante de compra",
        required=False
    )
    
    fecha_compra = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label="Fecha de Compra",
        help_text="Fecha en que se realizó la compra",
        required=False
    )
    
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'categoria', 'unidad_medida', 'stock_minimo', 'precio_unitario', 'descripcion']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: AME001, FRG002, etc.'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'unidad_medida': forms.Select(attrs={
                'class': 'form-select'
            }),
            'stock_minimo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción opcional del producto'
            })
        }


class EntradaStockForm(forms.ModelForm):
    """Formulario para registrar entrada de stock (compra)"""
    
    class Meta:
        model = EntradaStock
        fields = ['numero_entrada', 'tipo', 'proveedor', 'fecha_compra', 'comprobante', 'total_compra', 'observaciones']
        widgets = {
            'numero_entrada': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de factura o boleta'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'proveedor': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_compra': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'comprobante': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'total_compra': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones adicionales'
            })
        }


class DetalleEntradaForm(forms.ModelForm):
    """Formulario para detalles de entrada de stock"""
    
    class Meta:
        model = DetalleEntradaStock
        fields = ['producto', 'area_destino', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'area_destino': forms.Select(attrs={
                'class': 'form-select'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.01',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': '0.00'
            })
        }


class ProveedorForm(forms.ModelForm):
    """Formulario para agregar proveedores"""
    
    class Meta:
        model = Proveedor
        fields = ['nombre', 'rut', 'telefono', 'email', 'direccion', 'contacto']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del proveedor'
            }),
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12.345.678-9'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 1234 5678'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@proveedor.com'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Dirección del proveedor'
            }),
            'contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del contacto principal'
            })
        }


# Formset para manejar múltiples productos en una entrada
DetalleEntradaFormSet = forms.inlineformset_factory(
    EntradaStock,
    DetalleEntradaStock,
    form=DetalleEntradaForm,
    extra=1,
    min_num=1,
    can_delete=True
)