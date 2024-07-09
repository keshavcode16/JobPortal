from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, Boolean
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk
from .models import JobPost

# Define a connection to Elasticsearch
connections.create_connection(hosts=['localhost'])

class JobPostDocument(Document):
    title = Text()
    description = Text()
    skills = Keyword(multi=True)
    slug = Keyword()
    experience_years = Integer()
    experience_months = Integer()
    created_by = Integer()
    qualification = Keyword(multi=True)
    vacancies = Integer()
    created_on = Date()
    modified_on = Date()
    status = Boolean()

    class Index:
        name = 'jobpost_index'

    def save(self, **kwargs):
        return super().save(**kwargs)

    @classmethod
    def index_all(cls):
        bulk_indexing()  # Define this function to bulk index all JobPost instances

    @classmethod
    def search(cls, **kwargs):
        # Implement search functionality here
        pass

    class Meta:
        model = JobPost


def bulk_indexing():
    JobPostDocument.init()
    bulk(client=connections.get_connection(), actions=[
        {
            '_op_type': 'index',
            '_index': JobPostDocument._index._name,
            '_id': job_post.id,
            '_source': {
                'title': job_post.title,
                'description': job_post.description,
                'skills': [skill.name for skill in job_post.skills.all()],
                'slug': job_post.slug,
                'experience_years': job_post.experience_years,
                'experience_months': job_post.experience_months,
                'created_by': job_post.created_by.id,
                'qualification': [qualification.name for qualification in job_post.qualification.all()],
                'vacancies': job_post.vacancies,
                'created_on': job_post.created_on,
                'modified_on': job_post.modified_on,
                'status': job_post.status,
            }
        }
        for job_post in JobPost.objects.all()
    ])