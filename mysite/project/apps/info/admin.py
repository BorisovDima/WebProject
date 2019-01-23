from django.contrib import admin
from .models import InfoModel, Question, QuestionAdmin


admin.site.register(InfoModel)
admin.site.register(Question, QuestionAdmin)