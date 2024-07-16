from rest_framework import permissions
from core_apps.jobapp.models import JobPost
from .documents import JobPostDocument
from .serializers import JobSearchSerializer
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend, 
    IdsFilterBackend,
    SearchFilterBackend, 
    OrderingFilterBackend,
    DefaultOrderingFilterBackend, 
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet



class SearchJobView(DocumentViewSet):
    document = JobPostDocument
    serializer_class = JobSearchSerializer
    permission_classes = [permissions.AllowAny]
    # index_models = [JobPost]
    filter_backends = [FilteringFilterBackend, IdsFilterBackend, SearchFilterBackend, OrderingFilterBackend,  DefaultOrderingFilterBackend]
    loockup_field = "id"
    search_fields = ["title", "slug",  "skills", "qualification", "description"]
    filter_fields = {"skills": "skills", "qualification":"qualification"}
    ordering_fields = {"created_on": "created_on"}
    ordering = ("-created_on",)
