# Document Analysis SaaS

A powerful document analysis platform that provides PDF/text summarization, semantic search, and automated Q&A capabilities.

## Features

- PDF and Text Document Processing
- Document Summarization
- Semantic Search using Weaviate Vector Database
- Automated Q&A System
- Modern UI with Tailwind CSS and Shadcn UI

## Tech Stack

- Backend: Django + Django REST Framework
- Frontend: React + Tailwind CSS + Shadcn UI
- Vector Database: Weaviate
- Task Queue: Celery + Redis
- Storage: AWS S3 (optional)

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
WEAVIATE_URL=your-weaviate-url
WEAVIATE_API_KEY=your-weaviate-api-key
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

6. Start Celery worker (in a separate terminal):
```bash
celery -A docsaas worker -l info
```

## Project Structure

```
docsaas/
├── backend/
│   ├── api/
│   ├── documents/
│   ├── qa/
│   └── search/
├── frontend/
│   ├── src/
│   └── public/
└── manage.py
```

## API Documentation

The API documentation is available at `/api/docs/` when running the development server.

## License

MIT License 