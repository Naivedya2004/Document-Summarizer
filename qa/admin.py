from django.contrib import admin
from .models import Question, Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('document', 'user', 'question_text', 'created_at', 'is_answered')
    list_filter = ('is_answered', 'created_at')
    search_fields = ('question_text',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at', 'confidence_score')
    list_filter = ('created_at',)
    search_fields = ('answer_text',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
