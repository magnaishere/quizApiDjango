from rest_framework import viewsets
from .serializers import QuizSerializer, QuestionSerializer, AnswerSerializer, UserResultSerializer, TemporizerSerializer
from .models import Quiz, Question, Answer, UserResult, Temporizer
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
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
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from .schemas import step_quiz_schema, QuizStepByUserSchema
from .email import BalanceEmailService
import datetime

# Vistas de quiz SOLO SUPERUSERS()
class QuizView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser,]
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()
    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        for i, data in enumerate(response.data):
            item = response.data[i]
            item['questions'] = QuestionSerializer(Question.objects.filter(quiz=data["id"]), many=True).data
        return response

    
# Vistas de quiz SOLO SUPERUSERS()
@parser_classes((MultiPartParser,))  
class QuestionView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser,] 
    serializer_class = QuestionSerializer
    my_tags = ["Questions"]
    @swagger_auto_schema(manual_parameters=[openapi.Parameter('answers', openapi.IN_QUERY, description="Respuestas separadas por (,) por ejemplo: answer1,answer2,answer3,answer4", required=True, type=openapi.TYPE_STRING)])
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
    
    
# Vistas de answers result Solo GET y SUPERUSERS()
class AnswerView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser,]
    http_method_names = ['get']
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()         

# Vistas de userResult Solo GET y SUPERUSERS()
class UserResultView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser,]
    http_method_names = ['get']
    serializer_class = UserResultSerializer
    queryset = UserResult.objects.all()
    
# Método personalizado para realizar un quiz Solo usuarios autenticados
@swagger_auto_schema(tags=['Método para hacer un quiz'], request_body=step_quiz_schema, responses=QuizStepByUserSchema, method='POST')
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def QuizStepByUser(request):
    user = get_object_or_404(User, id = request.data['user'])
    if not user:
        return Response({"error": "Usuario no válido"}, status=status.HTTP_400_BAD_REQUEST)
    quiz = get_object_or_404(Quiz, id = request.data['quiz'])
    if not quiz:
        return Response({"error": "Quiz no válido"}, status=status.HTTP_400_BAD_REQUEST)
    answers = Answer.objects.filter(quiz=request.data['quiz'], user=user)
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
        serializerAnswer = AnswerSerializer(data={'quiz': quiz.id, 'question': oldQuestion[0], 'user': user.id, 'answer': request.data['answer']})
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

                        
                        
                        
                        
