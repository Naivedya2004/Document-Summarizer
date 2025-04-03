from django.contrib import admin
from .models import Document, DocumentChunk

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_type', 'uploaded_by', 'uploaded_at', 'is_processed', 'file_size', 'page_count')
    list_filter = ('document_type', 'is_processed', 'uploaded_at')
    search_fields = ('title', 'summary')
    readonly_fields = ('file_size', 'uploaded_at')
    ordering = ('-uploaded_at',)

@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ('document', 'chunk_index', 'created_at')
    list_filter = ('document', 'created_at')
    search_fields = ('content',)
    readonly_fields = ('created_at',)
    ordering = ('document', 'chunk_index')
