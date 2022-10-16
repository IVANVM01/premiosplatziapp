from django.urls import path
from . import views                 #Desde la carpeta actual, que es un paquete, importar las vistas

app_name = "polls"
urlpatterns = [
    #ex: /polls/
    path("", views.index, name="index"),
    #ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),  #El valor definido en name es el que se usa con la etiqueta url en el archivo html
    #ex: /polls/5/results
    path("<int:question_id>/results/", views.results, name="results"),
    #ex: /polls/5/vote
    path("<int:question_id>/vote/", views.vote, name="vote"),
]