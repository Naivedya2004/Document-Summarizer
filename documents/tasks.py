from django.conf import settings
import PyPDF2
import io
from .models import Document, DocumentChunk

def process_document(document_id):
    """
    Process a document synchronously without vector storage
    """
    try:
        document = Document.objects.get(id=document_id)
        
        # Read the document content
        content = ""
        if document.document_type == 'pdf':
            pdf_reader = PyPDF2.PdfReader(document.file)
            document.page_count = len(pdf_reader.pages)
            for page in pdf_reader.pages:
                content += page.extract_text() + "\n"
        else:
            content = document.file.read().decode('utf-8')

        # Create chunks (simple implementation - can be improved with better chunking strategies)
        chunks = [content[i:i + 1000] for i in range(0, len(content), 1000)]

        # Store chunks in database
        for index, chunk_content in enumerate(chunks):
            DocumentChunk.objects.create(
                document=document,
                content=chunk_content,
                chunk_index=index
            )

        # Create a simple summary (first 500 characters)
        document.summary = content[:500] + "..." if len(content) > 500 else content
        document.is_processed = True
        document.save()

        return True

    except Exception as e:
        # Handle errors appropriately
        print(f"Error processing document {document_id}: {str(e)}")
        return False 