from django.contrib import admin

# Register your models here.
from questions.models import Question

class QuestionModelAdmin(admin.ModelAdmin):
    """docstring for QuestionModelAdmin"""
    list_display = ['__unicode__', 'text']
    class Meta:
        model = Question


admin.site.register(Question, QuestionModelAdmin)
