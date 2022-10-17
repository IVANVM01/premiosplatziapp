# Es una buena practica separar los imports de python nativo de los de django
import datetime

from django.test import TestCase
from django.utils import timezone

from . models import Question

# Create your tests here.
class QuestionModelTests(TestCase):
    question_text = "¿Quién es el mejor Course Director de Platzi?"

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        question = Question(question_text=self.question_text, pub_date=time)
        self.assertIs(question.was_published_recently(), False)
        # Afirmo que el resultado del metodo .was_published_recently() es Falso

    def test_was_published_recently_with_past_questions_with_one_day_or_less(self):
        """was_published_recently returns True for questions whose pub_date is one day or less in the past"""
        time = timezone.now() - datetime.timedelta(hours=23)
        question = Question(question_text=self.question_text, pub_date=time)
        self.assertIs(question.was_published_recently(), True)
        # Afirmo que el resultado del metodo .was_published_recently() es Verdadero

    def test_was_published_recently_with_past_questions_with_more_than_one_day(self):
        """was_published_recently returns False for questions whose pub_date is more than one day in the past"""
        time = timezone.now() - datetime.timedelta(days=2)
        question = Question(question_text=self.question_text, pub_date=time)
        self.assertIs(question.was_published_recently(), False)
        # Afirmo que el resultado del metodo .was_published_recently() es Falso

    def test_was_published_recently_with_questions_of_now(self):
        """was_published_recently returns True for questions whose pub_date is now"""
        time = timezone.now()
        question = Question(question_text=self.question_text, pub_date=time)
        self.assertIs(question.was_published_recently(), True)
        # Afirmo que el resultado del metodo .was_published_recently() es Verdadero


# assert condition, msg error
#assert len(string) > 0, "No se puede ingresar una cadena vacia"
# Afirmo que la logitud del string es mayor que cero, sino corte el programa e imprima el mensaje