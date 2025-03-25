from celery import shared_task
from django.utils import timezone
from .models import Documento
from .services.document_processor import DocumentProcessor

@shared_task
def procesar_documento(documento_id: int):
    """
    Tarea Celery para procesar un documento de forma asíncrona.
    
    Args:
        documento_id: ID del documento a procesar
    """
    try:
        # Obtener el documento
        documento = Documento.objects.get(id=documento_id)
        
        # Procesar el documento
        processed_data = DocumentProcessor.process(documento.archivo.path)
        
        # Actualizar el documento con los resultados
        documento.contenido_procesado = processed_data
        documento.formato = processed_data.get('tipo', 'desconocido')
        documento.fecha_procesado = timezone.now()
        documento.save()
        
        return {
            'status': 'success',
            'documento_id': documento_id,
            'mensaje': 'Documento procesado correctamente'
        }
        
    except Documento.DoesNotExist:
        return {
            'status': 'error',
            'mensaje': f'No se encontró el documento con ID {documento_id}'
        }
    except Exception as e:
        return {
            'status': 'error',
            'mensaje': f'Error procesando documento: {str(e)}'
        }
