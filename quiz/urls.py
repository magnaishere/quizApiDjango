from django.urls import path, include, re_path
from rest_framework import routers
from quiz import views

router = routers.DefaultRouter()
router.register(r'quiz', views.QuizView, basename='quiz')
router.register(r'question', views.QuestionView, basename='card')
router.register(r'answer', views.AnswerView, basename='cards')
router.register(r'result', views.UserResultView, basename='result')

urlpatterns = [
    path('api/', include(router.urls)),
    re_path('api/quiz_actions', views.QuizStepByUser),
]
