from django.contrib import admin
from .models import Quiz, Question, Answer, UserResult, Temporizer

# Register your models here.
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserResult)
admin.site.register(Temporizer)

