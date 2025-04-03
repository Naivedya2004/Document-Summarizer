from django.contrib import admin
from .models import SearchQuery, SearchResult

@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('user', 'query_text', 'created_at', 'results_count', 'execution_time')
    list_filter = ('created_at',)
    search_fields = ('query_text',)
    readonly_fields = ('created_at', 'execution_time')
    ordering = ('-created_at',)

@admin.register(SearchResult)
class SearchResultAdmin(admin.ModelAdmin):
    list_display = ('search_query', 'document', 'rank', 'relevance_score')
    list_filter = ('search_query', 'document')
    search_fields = ('search_query__query_text',)
    ordering = ('search_query', 'rank')
