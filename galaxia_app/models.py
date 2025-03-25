from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Documento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='documentos/')
    formato = models.CharField(max_length=50, blank=True)
    contenido_procesado = models.JSONField(blank=True, null=True)
    resumen_ia = models.TextField(blank=True)
    categorias_ia = models.JSONField(blank=True, null=True)
    fecha_procesado = models.DateTimeField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto-rellenar el título si está vacío
        if not self.titulo and self.archivo:
            self.titulo = self.archivo.name.split('/')[-1]
        
        # Auto-detectar el formato
        if self.archivo and not self.formato:
            self.formato = self.archivo.name.split('.')[-1].lower()
        
        super().save(*args, **kwargs)
        
        # Encolar el procesamiento del documento
        from .tasks import procesar_documento
        if not self.contenido_procesado:
            procesar_documento.delay(self.id)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['-fecha_creacion']
