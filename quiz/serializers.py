from rest_framework import serializers
from .models import Quiz, Question, Answer, UserResult, Temporizer
from django.conf import settings
from drf_yasg import openapi
from django.contrib.auth import get_user_model

class AnswersMessageField(serializers.CharField):
    class Meta:
         swagger_schema_fields = {
            "type": openapi.TYPE_STRING,
            "title": "answers",
            "description": "Respuestas separadas por (,) por ejemplo: answer1,answer2,answer3,answer4"
         }
   
class QuestionSerializer(serializers.ModelSerializer):
      answers = AnswersMessageField()
      class Meta: 
         model = Question
         exclude = ('imgname', )
      

class QuizSerializer(serializers.ModelSerializer):
      questions = QuestionSerializer(many=True, read_only=True)
      class Meta: 
         model = Quiz
         fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
      class Meta: 
         model = Answer
         fields = ('__all__')
        
class UserResultSerializer(serializers.ModelSerializer):
     class Meta: 
        model = UserResult
        fields = '__all__'
        
class TemporizerSerializer(serializers.ModelSerializer):
      class Meta: 
         model = Temporizer
         fields = '__all__'
      