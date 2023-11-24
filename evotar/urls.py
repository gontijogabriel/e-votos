# evotar urls.py
from django.urls import path
from evotar.views import index

urlpatterns = [
    path('', index, name='index'),
]