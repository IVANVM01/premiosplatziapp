from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from . models import Question, Choice


# Create your views here.

"""[polls/views/index]
Args:
    request ([HTTP]): [Request]
Returns:
    [Render]: [Request, Url, Dict(Question.objects.all())]
"""
# FUNCTION BASED VIEW
"""
def index(request):
    #return HttpResponse("Estás en la página principal de Premios Platzi App")

    # Crea una consulta de todos los objetos del modelo haciendo uso del ORM de Django
    latest_question_list = Question.objects.all()
    context = {
        "latest_question_list": latest_question_list
    }
    
    # Retorna el template que se desea; como parametros se pasa la petición,
    # la ruta del template (Django junta las carpetas template de todas las aplicaciones, por lo que solo se requiere indicar la ruta interna partiendo de la carpeta template),
    # y un contexto que son un conjuno de variables en un diccionario disponibles para uso en el template
    return render(request, "polls/index.html", context)
"""
# CLASS BASED VIEW:             http://ccbv.co.uk/
class IndexView(generic.ListView):
    template_name = "polls/index.html"              # Esto se corresponde con el segundo parametro de render - (atributo de la clase)
    context_object_name = "latest_question_list"    # Esto se corresponde con el tercer parametro de render, definiendo el nombre con que se van a pasar los datos por context - (atributo de la clase)

    def get_queryset(self): # Recibe self como parametro porque es el metodo de una clase. Realiza la operación de la consulta
        #return Question.objects.all()
        """Return the last five published questions"""
        # El menos(-) al principio es para ordenar desde las mas recientes a las mas antiguas. Se hace un rebanado o slicing de los 5 primeros resultados
        return Question.objects.order_by("-pub_date")[:5] # Estos son los datos que se van a guardar con el nombre "latest_question_list"


# FUNCTION BASED VIEW
"""
def detail(request, question_id):
    #return HttpResponse(f"Estás viendo la pregunta número {question_id}")

    # Si la consulta es vacia, la pagina mostrará el error DoesNotExist, en su lugar se usa el atajo get_object_or_404 que permite controlar el error elevando el 404
    #question = Question.objects.get(pk=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {
        "question": question
    }
    return render(request, "polls/detail.html", context)
"""
# CLASS BASED VIEW
class DetailView(generic.DeleteView):   # Circunstancial que el nombre de la clase propia se llama igual que la clase de la que hereda
    model = Question                    # Solo con definir este atributo, Django por debajo hace toda la consulta correspondiente
    template_name = "polls/detail.html" # Solo con definir este atributo, Django por debajo hace el return render, definiendo el nombre con que se van a pasar los datos ya consultados


# FUNCTION BASED VIEW
"""
def results(request, question_id):
    #return HttpResponse(f"Estás viendo los resultados de la pregunta número {question_id}")

    question = get_object_or_404(Question, pk=question_id)
    context = {
        "question": question
    }
    return render(request, "polls/results.html", context)
"""
# CLASS BASED VIEW
class ResultView(generic.DeleteView):
    model = Question                    # Solo con definir este atributo, Django por debajo hace toda la consulta correspondiente
    template_name = "polls/results.html"# Solo con definir este atributo, Django por debajo hace el return render, definiendo el nombre con que se van a pasar los datos ya consultados


def vote(request, question_id):
    #return HttpResponse(f"Estás votando a la pregunta número {question_id}")

    question = get_object_or_404(Question, pk=question_id)
    try:                                        # INTENTAR:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        # choice es la key (name) que referencia al value (choice.id) en el diccionario llamado POST del objeto request, que tiene la informacion de la respuesta seleccionada
    except (KeyError, Choice.DoesNotExist):     # SI LA EJECUCION FALLA:
        # KeyError: Por si en el diccionario POST de la request no existe una llave con nombre choice porque no se eligió una respuesta
        # Choice.DoesNotExist: Por si el metodo get no encuentra una respuesta con el choice.id dado
        context = {
            "question": question,
            "error_message": "No elegiste una respuesta"
        }
        return render(request, "polls/detail.html", context)
    else:                                       # SI LA EJECUCION ES EXITOSA:
        selected_choice.votes += 1
        selected_choice.save() # Guarda la modificación
        # Una buena practica al trabajar con formularios es redirigir al usuario a una nueva pagina,
        # el redirect se asegura de que el usuario no envie la informacion dos veces en el formulario
        # El metodo reverse en python es el equivalente de la etiqueta url del Django_Templete_System para no Hard-Codear una url
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,))) #args es una tupla, en este caso de 1 elemento (por eso la coma al final)