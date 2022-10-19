from django.contrib import admin
from . models import Choice, Question

# Esta clase permite la opcion de agregar respuestas al momento de crear preguntas
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3 # Tres respuestas por defecto

# Las clases que se creen con el nombre de un modelo y la palabra admin sirven para editar como se ve ese modelo en el administrador de Django
class QuestionAdmin(admin.ModelAdmin):
    # El atributo fields permite ajustar el orden de aparicion de los campos del modelo
    fields = ["pub_date", "question_text"]
    # El atributo inlines permite vicular la clase ChoiceInline en QuestionAdmin
    inlines = [ChoiceInline]
    # El atributo list_display permite afectar como se ve la lista del modelo
    # La forma por defecto como se muestran las preguntas viene dado por como se definio el metodo __str__ del modelo, este atributo modifica esa forma por defecto
    list_display = ("question_text", "pub_date", "was_published_recently")
    # Para realizar un filtrado a los datos que se van a mostrar se utiliza el atributo list_filter. Esto coloca un cuadro de filtrado en el administrador
    list_filter = ["pub_date"]
    # Con eltaributo se puede poner un cuadro de busqueda
    search_fields = ["question_text"]
    # Para mas atributos: https://docs.djangoproject.com/en/4.0/ref/contrib/admin/

#admin.site.register(Question) # Hace disponible el modelo dentro del administrador para que otras personas puedan editarlo
# Para registrar uno o mas modelos se pueden pasar dentro de una lista:
#admin.site.register([Question, Choice])
# Para que el modelo lleve la reglas definidas en las clases ModeloAdmin, como segundo parametro se debe pasar esa clase
admin.site.register(Question, QuestionAdmin)