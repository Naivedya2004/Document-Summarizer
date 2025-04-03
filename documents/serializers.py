from rest_framework import serializers
from .models import Document, DocumentChunk

class DocumentChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentChunk
        fields = ['id', 'content', 'chunk_index', 'vector_id', 'created_at']
        read_only_fields = ['vector_id', 'created_at']

class DocumentSerializer(serializers.ModelSerializer):
    chunks = DocumentChunkSerializer(many=True, read_only=True)
    uploaded_by = serializers.ReadOnlyField(source='uploaded_by.username')

    class Meta:
        model = Document
        fields = [
            'id', 'title', 'file', 'document_type', 'uploaded_by',
            'uploaded_at', 'summary', 'vector_id', 'is_processed',
            'file_size', 'page_count', 'chunks'
        ]
        read_only_fields = [
            'uploaded_by', 'uploaded_at', 'summary', 'vector_id',
            'is_processed', 'file_size', 'page_count'
        ] 