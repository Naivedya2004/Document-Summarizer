from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Document, DocumentChunk
from .serializers import DocumentSerializer, DocumentChunkSerializer
from .forms import DocumentForm
from .tasks import process_document

# Create your views here.

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Save the document and associate it with the current user
        document = serializer.save(uploaded_by=self.request.user)
        # Process the document synchronously
        success = process_document(document.id)
        if not success:
            return Response(
                {'error': 'Failed to process document'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def reprocess(self, request, pk=None):
        document = self.get_object()
        success = process_document(document.id)
        if success:
            return Response({'status': 'Document processed successfully'})
        return Response(
            {'error': 'Failed to process document'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def get_queryset(self):
        # Filter documents by the current user
        return Document.objects.filter(uploaded_by=self.request.user)

class DocumentChunkViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DocumentChunkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        document_id = self.kwargs.get('document_id')
        document = get_object_or_404(Document, id=document_id, uploaded_by=self.request.user)
        return DocumentChunk.objects.filter(document=document)

@login_required
def document_list(request):
    documents = Document.objects.all().order_by('-uploaded_at')
    return render(request, 'documents/document_list.html', {'documents': documents})

@login_required
def document_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            messages.success(request, 'Document uploaded successfully.')
            return redirect('documents:document_list')
    else:
        form = DocumentForm()
    return render(request, 'documents/document_upload.html', {'form': form})

@login_required
def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    return render(request, 'documents/document_detail.html', {'document': document})

@login_required
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Document deleted successfully.')
        return redirect('documents:document_list')
    return render(request, 'documents/document_confirm_delete.html', {'document': document})
