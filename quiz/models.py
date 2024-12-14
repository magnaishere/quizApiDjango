from django.db import models
from django.conf import settings

import datetime

def upload_to(instance, filename):
    return '/'.join(['images', str(instance.imgname), filename])
    
# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    limit_time = models.IntegerField(default=300)
    def __str__(self):
        return self.title

class Question(models.Model):
    question = models.TextField()
    quiz = models.ForeignKey(
        Quiz,
        null=False,
        on_delete=models.CASCADE,
        related_name='%(class)s_requests_quiz'
    )
    imgname = models.TextField(default='')
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    answers = models.TextField(default='')
    correct = models.CharField(max_length=200)
    def __str__(self):
        return 'Quiz: ' + str(self.quiz) + ' Question: ' + self.question
    
class Answer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        on_delete=models.CASCADE,
        related_name='%(class)s_requests_answer_user'
    )
    question = models.ForeignKey(
        Question,
        null=False,
        on_delete=models.CASCADE,
        related_name='%(class)s_requests_answer_question'
    )
    quiz = models.ForeignKey(
        Quiz,
        null=False,
        on_delete=models.CASCADE,
        related_name='%(class)s_requests_answer_quiz'
    )
    answer = models.CharField(max_length=200)
    def __str__(self):
        return 'User: ' + str(self.user) + ' Answer: ' + str(self.answer)   

class UserResult(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        on_delete=models.CASCADE,
        related_name='%(class)s_requests_user_result'
    )
    quiz = models.ForeignKey(
        Quiz,
        null=False,
        on_delete=models.CASCADE,
        related_name='%(class)s_requests_question_result'
    )
    total_points = models.FloatField()
    def __str__(self):
        return 'User: ' + str(self.user) + ' Quiz: ' + str(self.quiz)

class Temporizer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        on_delete=models.CASCADE,
        related_name='%(class)s_requests_user_temp'
    )
    quiz = models.ForeignKey(
        Quiz,
        null=False,
        on_delete=models.CASCADE,
        related_name='%(class)s_requests_quiz_temp'
    )
    start_quiz_time = models.DateTimeField(default=datetime.datetime.now)
    total_exec_time = models.IntegerField(default=0)