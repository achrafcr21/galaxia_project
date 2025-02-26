from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Waitlist
from django.core.mail import send_mail
from django.conf import settings

@csrf_exempt  # Desactiva temporalmente CSRF para pruebas
def join_waitlist(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")

            if not email:
                return JsonResponse({"error": "Email is required"}, status=400)

            # Verificar si el email ya está registrado
            if Waitlist.objects.filter(email=email).exists():
                return JsonResponse({"error": "This email is already in the waitlist"}, status=400)

            # Guardar en la base de datos
            Waitlist.objects.create(email=email)

            # Enviar correo de confirmación
            send_mail(
                "¡Bienvenido a la lista de espera!",
                "Gracias por unirte a nuestra waitlist. Te avisaremos cuando haya novedades.",
                settings.EMAIL_HOST_USER,  # Desde el email configurado en settings.py
                [email],  # Correo del usuario que se registró
                fail_silently=False,
            )

            return JsonResponse({"message": "Successfully added to waitlist and email sent!"}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


def get_waitlist(request):
    emails = list(Waitlist.objects.values_list('email', flat=True))
    return JsonResponse({"waitlist": emails}, safe=False)