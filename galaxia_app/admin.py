from django.contrib import admin
from .models import Documento

# Register your models here.

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'formato', 'fecha_procesado', 'fecha_creacion')
    list_filter = ('formato', 'fecha_procesado', 'fecha_creacion')
    search_fields = ('titulo', 'usuario__username')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'fecha_procesado')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si el objeto ya existe
            return self.readonly_fields + ('archivo',)  # No permitir cambiar el archivo
        return self.readonly_fields
