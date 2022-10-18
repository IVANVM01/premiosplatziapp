from django.urls import path
from . import views                 #Desde la carpeta actual, que es un paquete, importar las vistas

app_name = "polls"
urlpatterns = [
    # FUNCTION BASED VIEW: Llama a las funciones definidas en views.py
    # ex: /polls/
    #path("", views.index, name="index"),
    # ex: /polls/5/
    #path("<int:question_id>/", views.detail, name="detail"),  #El valor definido en name es el que se usa con la etiqueta url en el archivo html
    # ex: /polls/5/results
    #path("<int:question_id>/results/", views.results, name="results"),

    # CLASS BASED VIEW: Llama a las clases definidas en views.py. Se requiere el metodo .as_view().
    # Django no puede leer automaticamente el parametro question_id en la url (no sabe el nombre con el que se espera puesto que no esta definido en la clase)
    # Entonces se define como pk, así sabrá que el parametro es la primary key para ejecutar la consulta
    # ex: /polls/
    path("", views.IndexView.as_view(), name="index"),
    # ex: /polls/5/
    path("<int:pk>/detail/", views.DetailView.as_view(), name="detail"),  #El valor definido en name es el que se usa con la etiqueta url en el archivo html
    # ex: /polls/5/results
    path("<int:pk>/results/", views.ResultView.as_view(), name="results"),

    # ex: /polls/5/vote
    path("<int:question_id>/vote/", views.vote, name="vote"),
]