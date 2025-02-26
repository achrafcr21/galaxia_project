from django.urls import path
from .views import join_waitlist, get_waitlist  # ✅ Agregamos get_waitlist

urlpatterns = [
    path('join/', join_waitlist, name='join_waitlist'),
    path('', get_waitlist, name='get_waitlist'),
]