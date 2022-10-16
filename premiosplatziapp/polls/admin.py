from django.contrib import admin
from . models import Question

admin.site.register(Question) # Hace disponible el modelo dentro del administrador para que otras personas puedan editarlo
#Para registrar uno o mas modelos puedes pasarlos dentro de una lista:
#admin.site.register([Question, Choice])