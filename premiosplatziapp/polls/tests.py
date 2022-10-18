# Es una buena practica separar los imports de python nativo de los de django
# Se utilizan dos enter para separar funciones y clases
# Se utiliza un solo enter para separar metodos dentro de una clase

import datetime

from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

from . models import Question


# TEST FOR MODELS
class QuestionModelTests(TestCase):
    # El test no se aplica sobre los datos que puedan estar actualmente en la DB real,
    # sino que se aplica sobre una DB de pruebas con datos creados en el mismo test que inducen la situacion que se quiere probar
    question_text = "¿Quién es el mejor Course Director de Platzi?"

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        question = Question(question_text=self.question_text, pub_date=time)
        self.assertIs(question.was_published_recently(), False)
        # Afirmo que el resultado del metodo .was_published_recently() es Falso

    def test_was_published_recently_with_past_questions_with_one_day_or_less(self):
        """was_published_recently returns True for questions whose pub_date is one day or less in the past."""
        time = timezone.now() - datetime.timedelta(hours=23)
        question = Question(question_text=self.question_text, pub_date=time)
        self.assertIs(question.was_published_recently(), True)
        # Afirmo que el resultado del metodo .was_published_recently() es Verdadero

    def test_was_published_recently_with_past_questions_with_more_than_one_day(self):
        """was_published_recently returns False for questions whose pub_date is more than one day in the past."""
        time = timezone.now() - datetime.timedelta(days=2)
        question = Question(question_text=self.question_text, pub_date=time)
        self.assertIs(question.was_published_recently(), False)
        # Afirmo que el resultado del metodo .was_published_recently() es Falso

    def test_was_published_recently_with_questions_of_now(self):
        """was_published_recently returns True for questions whose pub_date is now."""
        time = timezone.now()
        question = Question(question_text=self.question_text, pub_date=time)
        self.assertIs(question.was_published_recently(), True)
        # Afirmo que el resultado del metodo .was_published_recently() es Verdadero


def create_question(question_text, days): 
    """
    Create a question with the given 'question_text' and published with the given number
    of 'days' offset to now (negative for questions published in the past, positive for
    questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


#TEST FOR VIEWS
class QuestionIndexViewTests(TestCase):
    # El test no se aplica sobre los datos que puedan estar actualmente en la DB real,
    # sino que se aplica sobre una DB de pruebas con datos creados en el mismo test que inducen la situacion que se quiere probar

    # Se va testear que cuando no haya preguntas en la DB, la app de la respuesta correcta: "No polls are avaliable."
    # Por tanto, para inducir esa situación, no se insertaron preguntas durante la ejecución de este test
    def test_no_question(self):
        """If no question exist, an appropiate message is displayed."""
        response = self.client.get(reverse("polls:index")) # self.client.get hace una peticion HTTP de tipo GET sobre el index, guardando el resultado en el atributo response
        # En este caso que hay varios asserts, deben pasar los tres para que la prueba sea exitosa
        self.assertEqual(response.status_code, 200) # Verifica que el status_code de la respuesta es exitoso
        # Afirmo que el status_code de le respuesta es igual a 200 (exitoso)
        self.assertContains(response, "No polls are avaliable.") # Ese mensaje esta definido en el index.html si no hay preguntas para mostrar (latest_question_list este vacio), que es lo que se esta testeando. Es decir, se verifica que ese mensaje aparezca en la pag si no hay preguntas
        # Afirmo que la respuesta contiene el mensaje "No polls are avaliable."
        self.assertQuerysetEqual(response.context["latest_question_list"], []) # Verifica que el conjunto de preguntas que se trajo django esta vacio. "latest_question_list" es la key que referencia al value que contiene el Queryset que resulta de la consulta usando filter en la IndexView
        # Afirmo que el Queryset de la consulta es una lista vacia

    # RETO: Crear el test para verificar que la página no muestre preguntas del futuro
    def test_do_not_display_future_questions(self):
        """If there are questions with a pub_date greater than the current date in the DB, these questions should not be displayed."""
        # Agregar pregunta futura en la DB
        future_question = create_question("¿Quién es el mejor Course-Director de Platzi?", 30)
        # Simular peticion HTTP
        response = self.client.get(reverse("polls:index"))
        # Realizar tests:
            # Verificar respuesta exitosa
        self.assertEqual(response.status_code, 200)
            # Verificar que el QuerySet de la consulta es una lista vacia, ya que solo habría una pregunta, y es futura
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
            # Verificar que en pantalla aparezca el mensaje "No polls are avaliable.", ya que solo habría una pregunta, y es futura
        self.assertContains(response, "No polls are avaliable.")
            # Verificar que la pregunta futura no esté en el context del response
        self.assertNotIn(future_question, response.context["latest_question_list"])

    def test_display_past_questions(self):
        """If there are questions with a pub_date less than the current date in the DB, these questions should be displayed."""
        # Agregar pregunta pasada en la DB
        question = create_question("¿Quién es el mejor Course-Director de Platzi?", -10)
        # Simular peticion HTTP
        response = self.client.get(reverse("polls:index"))
        # Realizar tests:
            # Verificar respuesta exitosa
        self.assertEqual(response.status_code, 200)
            # Verificar que el QuerySet de la consulta contenga la pregunta insertada
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])
            # Verificar que la pregunta esté en el context del response
        self.assertIn(question, response.context["latest_question_list"])

    def test_future_question_and_past_question(self):
        """Even if both past and future question exist, only past questions are displayed."""
        past_question = create_question("Past question", -30)
        future_question = create_question("Future question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question])

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        question1 = create_question("Past question 1", -30)
        question2 = create_question("Past question 2", -5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question2, question1]) #El orden es al contrario porque la IndexView ordena desde la mas reciente (q2) a la mas antigua (q1). assertQuerysetEqual deja dependencia al orden de los objetos


# assert condition, msg_error
#assert len(string) > 0, "No se puede ingresar una cadena vacia"
# Afirmo que la logitud del string es mayor que cero, sino corte el programa e imprima el mensaje