from django.test import TestCase
from django.urls import reverse
import datetime
from django.utils import timezone
from .models import Question

# Create your tests here.
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - timezone.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - timezone.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    time = timezone.now() + timezone.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Polls are avaliable")
        self.assertQuerysetEqual(response.context["latest_questions_list"], [])

    def test_past_questions(self):
        create_question(question_text="Past Question", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_questions_list"], ["<Question : Past Question>"]
        )

    def test_future_question(self):
        create_question(question_text="Future Question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No Polls are avaliable")
        self.assertQuerysetEqual(response.context["latest_questions_list"], [])

    def future_question_and_past_question(self):
        create_question = Question(question_text="Past Question", days=-30)
        create_question = Question(question_text="Future Question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_questions_list"], ["<Question : Past Question>"]
        )

    def test_two_past_questions(self):
        create_question(question_text="Past Question 1", days=-30)
        create_question(question_text="Past Question 2", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_questions_list"],
            ["<Question : Past Question 2>", "<Question : Past Question 1>"],
        )
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text = "Future Question",days = 5)
        url = reverse('polls:detail',args=(future_question.id,))
        response = self.client.get(url)
        self.assertContains(response.status_code,404)
    def test_past_question(self):
        past_question = create_question(question_text = "Past Question",days = -5)
        url = reverse('polls:detail',args=(past_question.id,))    
        response = self.client.get(url)
        self.assertContains(response,past_question.question_text)


