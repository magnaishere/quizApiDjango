from rest_framework import viewsets
from .serializers import QuizSerializer, QuestionSerializer, AnswerSerializer, UserResultSerializer, TemporizerSerializer
from .models import Quiz, Question, Answer, UserResult, Temporizer
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import parser_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.models import User
from django import forms
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from .schemas import QuizStepByUserSchema
from .email import BalanceEmailService
import datetime

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

# Create your views here.
class QuizView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()
    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        for i, data in enumerate(response.data):
            item = response.data[i]
            item['questions'] = QuestionSerializer(Question.objects.filter(quiz=data["id"]), many=True).data
        return response

@parser_classes((MultiPartParser,))  
class QuestionView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] 
    serializer_class = QuestionSerializer
    my_tags = ["Questions"]
    @swagger_auto_schema(manual_parameters=[openapi.Parameter('answers', openapi.IN_FORM, description="Respuestas separadas por (,) por ejemplo: answer1,answer2,answer3,answer4", required=True, type=openapi.TYPE_STRING)])
    def create(self, request, *args, **kwargs):
        serializer = QuestionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({ 'status': 'error' }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        answers = serializer.data["answers"].split(',')
        return Response({
            'status': 'success', 
            'question': {
                "id" : serializer.data["id"], 
                "question" : serializer.data["question"],
                "image": serializer.data["image"] or '', 
                "answers": answers
            }}, status=status.HTTP_200_OK)
    queryset = Question.objects.all()
    
class AnswerView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

login_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'quiz': openapi.Schema(type=openapi.TYPE_INTEGER, description='id del quiz a ejecutar.'),
        'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='id del usuario actual.'),
        'answer': openapi.Schema(type=openapi.TYPE_STRING, description='Debe estar escrito de manera exacta al String de respuesta de lo contrario sera tomada como incorrecta por ejemplo=\'answer1\'. Solamente válido para responder a la pregunta. Este campo sera ignorado por el sistema en la primera ejecución.'),
    },
    required=['quiz', 'user']
)            

class UserResultView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated|ReadOnly]
    http_method_names = ['get']
    serializer_class = UserResultSerializer
    queryset = UserResult.objects.all()
@swagger_auto_schema(tags=['Método para hacer un quiz'], request_body=login_schema, responses=QuizStepByUserSchema, method='POST')
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def QuizStepByUser(request):
    user = get_object_or_404(User, id = request.query_params['user'])
    if not user:
        return Response({"error": "Usuario no válido"}, status=status.HTTP_400_BAD_REQUEST)
    quiz = get_object_or_404(Quiz, id = request.query_params['quiz'])
    if not quiz:
        return Response({"error": "Quiz no válido"}, status=status.HTTP_400_BAD_REQUEST)
    answers = Answer.objects.filter(quiz=request.query_params['quiz'], user=user)
    temps = Temporizer.objects.filter(quiz=quiz, user=user).order_by("id")
    if len(temps)==0:
        # Primera pregunta
        serializerTemp = TemporizerSerializer(data={ 'quiz': quiz.id, 'user': user.id })
        if not serializerTemp.is_valid():
            return Response({ 'status': 'error' }, status=status.HTTP_400_BAD_REQUEST)
        serializerTemp.save()
        firstQuestion = Question.objects.filter(quiz=quiz.id).order_by("id").values_list('id', 'question','image', 'answers')[0]
        return Response({
            'status': 'success', 
            'question': {
                "id" : firstQuestion[0], 
                "question" : firstQuestion[1],
                "image": firstQuestion[2] or '', 
                "answers": firstQuestion[3].split(',')
            }}, status=status.HTTP_200_OK)
    temp = temps[0]
    totaltime = (datetime.datetime.now() - temp.start_quiz_time.replace(tzinfo=None)).seconds
    temp.total_exec_time = totaltime
    temp.save()
    if totaltime > quiz.limit_time:
        answers.delete()
        Temporizer.objects.filter(quiz=quiz, user=user).delete()
        return Response({"error": "El tiempo para culminar el quiz ha concluido, por favor intente nuevamente"}, status=status.HTTP_400_BAD_REQUEST)
    allQuestions = Question.objects.filter(quiz=quiz).order_by("id").values_list('id', 'question','image', 'answers')
    if len(answers)+1 == len(allQuestions):
        # Quiz terminado calculando...
        success = 0
        for answ in answers:
            if answ.answer==answ.question.correct:
                success = success+1
        calification = (success*100)/len(allQuestions)
        try:
            serializerUserResult = UserResultSerializer(data={ 'quiz': quiz.id, 'user': user.id, 'total_points': calification })
            if not serializerUserResult.is_valid():
                return Response({ 'status': 'error' }, status=status.HTTP_400_BAD_REQUEST)
            serializerUserResult.save()
            Temporizer.objects.filter(quiz=quiz, user=user).delete()
            answers.delete()
            if BalanceEmailService(user.username, int(calification), str(len(allQuestions)), success, user.email):
                return Response({ 'status': 'success' }, status=status.HTTP_200_OK)
            else:
                return Response({ 'status': 'error' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(e)
            return Response({ 'status': 'error' }, status=status.HTTP_400_BAD_REQUEST)
    else:
        # No es primera pregunta calculamos la siguiente pregunta...
        newQuestion = allQuestions[len(answers)+1]
        oldQuestion = allQuestions[len(answers)]
        serializerAnswer = AnswerSerializer(data={'quiz': quiz.id, 'question': oldQuestion[0], 'user': user.id, 'answer': request.query_params['answer']})
        if not serializerAnswer.is_valid():
            return Response({ 'status': 'error' }, status=status.HTTP_400_BAD_REQUEST)
        serializerAnswer.save()
        return Response({
            'status': 'success', 
            'question': {
                "id" : newQuestion[0], 
                "question" : newQuestion[1],
                "image": newQuestion[2] or '', 
                "answers": newQuestion[3].split(',')
            }}, status=status.HTTP_200_OK)

                        
                        
                        
                        
