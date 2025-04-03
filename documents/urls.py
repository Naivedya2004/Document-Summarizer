from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, DocumentChunkViewSet
from . import views

router = DefaultRouter()
router.register(r'api', DocumentViewSet, basename='document')

app_name = 'documents'

urlpatterns = [
    # Template views
    path('', views.document_list, name='document_list'),
    path('upload/', views.document_upload, name='document_upload'),
    path('<int:pk>/', views.document_detail, name='document_detail'),
    path('<int:pk>/delete/', views.document_delete, name='document_delete'),
    
    # API endpoints
    path('', include(router.urls)),
    path('api/<int:document_id>/chunks/', DocumentChunkViewSet.as_view({'get': 'list'}), name='document-chunks'),
] 