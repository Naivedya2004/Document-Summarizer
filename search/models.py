from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class SearchQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    results_count = models.IntegerField(default=0)
    execution_time = models.FloatField(help_text="Search execution time in seconds")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Search: {self.query_text[:50]}..."

class SearchResult(models.Model):
    search_query = models.ForeignKey(SearchQuery, on_delete=models.CASCADE, related_name='results')
    document = models.ForeignKey('documents.Document', on_delete=models.CASCADE)
    document_chunk = models.ForeignKey('documents.DocumentChunk', on_delete=models.CASCADE)
    relevance_score = models.FloatField(help_text="Relevance score of the result (0-1)")
    rank = models.IntegerField(help_text="Position in search results")

    class Meta:
        ordering = ['rank']

    def __str__(self):
        return f"Result {self.rank} for search: {self.search_query.query_text[:30]}..."
