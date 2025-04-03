from django.db import models
from django.contrib.auth.models import User
from documents.models import Document
from django.utils import timezone

class Question(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='questions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_answered = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Question about {self.document.title}"

class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='answer')
    answer_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    confidence_score = models.FloatField(help_text="Confidence score of the answer (0-1)")
    source_chunks = models.ManyToManyField('documents.DocumentChunk', related_name='answers')

    def __str__(self):
        return f"Answer to question about {self.question.document.title}"
