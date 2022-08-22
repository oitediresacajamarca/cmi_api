from django.contrib import admin
from django.urls import path,include
from .views import consulta
urlpatterns = [
    path('<curso>/<agnio>/<mes>/<id_indicador>',consulta.as_view(),name='consulta'),
]
