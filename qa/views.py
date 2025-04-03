from django.shortcuts import get_object_or_404, render
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from documents.models import Document

# Create your views here.

class QuestionViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        Create a new question for a document
        """
        document_id = request.data.get('document_id')
        question_text = request.data.get('question')

        if not document_id or not question_text:
            return Response({
                'error': 'Both document_id and question are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get the document and verify ownership
        document = get_object_or_404(Document, id=document_id, uploaded_by=request.user)

        # Create the question
        question = Question.objects.create(
            document=document,
            user=request.user,
            question_text=question_text
        )

        # For now, create a simple answer based on document content
        # Later, we'll implement more sophisticated Q&A
        relevant_chunk = document.chunks.filter(
            content__icontains=question_text
        ).first()

        if relevant_chunk:
            answer = Answer.objects.create(
                question=question,
                answer_text=relevant_chunk.content[:500],
                confidence_score=0.5  # Placeholder confidence score
            )
            answer.source_chunks.add(relevant_chunk)
            question.is_answered = True
            question.save()

            return Response({
                'question_id': question.id,
                'question': question_text,
                'answer': answer.answer_text,
                'confidence_score': answer.confidence_score
            })
        else:
            return Response({
                'question_id': question.id,
                'question': question_text,
                'message': 'No relevant answer found in the document'
            }, status=status.HTTP_404_NOT_FOUND)

@login_required
def qa_view(request):
    documents = Document.objects.all()
    answer = None
    error = None
    
    if request.method == 'POST':
        document_id = request.POST.get('document')
        question_text = request.POST.get('question')
        
        try:
            document = Document.objects.get(id=document_id)
            
            # Create question
            question = Question.objects.create(
                user=request.user,
                document=document,
                text=question_text
            )
            
            # Generate answer (placeholder for now)
            answer = Answer.objects.create(
                question=question,
                content="This is a placeholder answer. The actual answer generation will be implemented using an LLM.",
                confidence=0.95
            )
            
        except Document.DoesNotExist:
            error = "Selected document not found."
        except Exception as e:
            error = str(e)
    
    return render(request, 'qa/qa.html', {
        'documents': documents,
        'answer': answer,
        'error': error
    })
