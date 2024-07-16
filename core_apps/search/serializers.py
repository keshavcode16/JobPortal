# from drf_haystack.serializers import HaystackSerializer
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import JobPostDocument

# from core_apps.search.search_indexes import ArticleIndex



class JobSearchSerializer(DocumentSerializer):
    class Meta:
        document = JobPostDocument
        fields = ["title", "slug",  "skills", "qualification", "description", "created_on"]




