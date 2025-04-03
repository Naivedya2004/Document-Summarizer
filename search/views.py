from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import SearchQuery, SearchResult
from documents.models import Document, DocumentChunk
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

class SearchViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        Perform a search across documents
        """
        query = request.data.get('query', '')
        if not query:
            return Response({'error': 'Query is required'}, status=status.HTTP_400_BAD_REQUEST)

        # For now, implement a simple text search
        chunks = DocumentChunk.objects.filter(
            content__icontains=query,
            document__uploaded_by=request.user
        ).select_related('document')[:10]

        # Create search query record
        search_query = SearchQuery.objects.create(
            user=request.user,
            query_text=query,
            results_count=len(chunks),
            execution_time=0.0  # We'll implement proper timing later
        )

        # Create search results
        results = []
        for i, chunk in enumerate(chunks):
            result = SearchResult.objects.create(
                search_query=search_query,
                document=chunk.document,
                document_chunk=chunk,
                relevance_score=1.0,  # We'll implement proper scoring later
                rank=i + 1
            )
            results.append({
                'document_title': chunk.document.title,
                'document_id': chunk.document.id,
                'chunk_content': chunk.content[:200] + '...' if len(chunk.content) > 200 else chunk.content,
                'rank': i + 1
            })

        return Response({
            'query': query,
            'results_count': len(results),
            'results': results
        })

@login_required
def search_view(request):
    query = request.GET.get('q', '')
    results = []
    
    if query:
        # Create search query
        search_query = SearchQuery.objects.create(
            user=request.user,
            query_text=query
        )
        
        # Perform search (simple contains for now, will be replaced with vector search)
        chunks = DocumentChunk.objects.filter(content__icontains=query)
        
        # Create search results
        for chunk in chunks:
            result = SearchResult.objects.create(
                search_query=search_query,
                document=chunk.document,
                content=chunk.content,
                score=1.0  # Placeholder score
            )
            results.append(result)
    
    return render(request, 'search/search.html', {
        'query': query,
        'results': results
    })
