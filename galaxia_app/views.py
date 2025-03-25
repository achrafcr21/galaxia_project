from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Documento
from .tasks import procesar_documento

# Create your views here.

@csrf_exempt  # Temporal para pruebas, en producción usar tokens CSRF
@login_required
def upload_documento(request):
    """
    Vista para subir documentos y procesarlos de forma asíncrona.
    """
    if request.method == 'POST' and request.FILES.get('documento'):
        try:
            file = request.FILES['documento']
            
            # Validar el formato del archivo
            formato = file.name.split('.')[-1].lower()
            if formato not in ['pdf', 'xlsx', 'xls', 'docx', 'doc']:
                return JsonResponse({
                    "status": "error",
                    "message": "Formato de archivo no soportado"
                }, status=400)
            
            # Crear el documento
            doc = Documento.objects.create(
                usuario=request.user,
                titulo=file.name,
                archivo=file
            )
            
            # Iniciar el procesamiento asíncrono
            procesar_documento.delay(doc.id)
            
            return JsonResponse({
                "status": "success",
                "message": "Documento subido correctamente",
                "documento_id": doc.id
            }, status=201)
            
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)
    
    return JsonResponse({
        "status": "error",
        "message": "Método no permitido o archivo no proporcionado"
    }, status=400)
