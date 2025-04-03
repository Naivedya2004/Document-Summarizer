from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('pdf', 'PDF'),
        ('txt', 'Text'),
        ('doc', 'Word Document'),
        ('docx', 'Word Document (New)'),
    ]

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPES)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(default=timezone.now)
    summary = models.TextField(blank=True, null=True)
    vector_id = models.CharField(max_length=255, blank=True, null=True)  # Weaviate vector ID
    is_processed = models.BooleanField(default=False)
    file_size = models.IntegerField(help_text="File size in bytes")
    page_count = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} ({self.document_type})"

    def save(self, *args, **kwargs):
        if not self.file_size:
            self.file_size = self.file.size
        super().save(*args, **kwargs)

class DocumentChunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')
    content = models.TextField()
    chunk_index = models.IntegerField()
    vector_id = models.CharField(max_length=255, blank=True, null=True)  # Weaviate vector ID
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['chunk_index']
        unique_together = ['document', 'chunk_index']

    def __str__(self):
        return f"Chunk {self.chunk_index} of {self.document.title}"
