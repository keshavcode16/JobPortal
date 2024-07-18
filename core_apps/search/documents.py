from django_elasticsearch_dsl import Document, fields
from core_apps.jobapp.models import JobPost
from django_elasticsearch_dsl.registries import registry




@registry.register_document
class JobPostDocument(Document):
    title = fields.TextField()
    description = fields.TextField()
    skills = fields.KeywordField()
    slug = fields.TextField()
    qualification = fields.KeywordField()

    class Index:
        name = 'jobpost_index'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = JobPost # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'created_on'
        ]

    def save(self, **kwargs):
        return super().save(**kwargs)

    def prepare_qualification(self, instance):
        return [qualification.name for qualification in instance.qualification.all()]
    
    def prepare_skills(self, instance):
        return [skill.name for skill in instance.skills.all()]

    class Meta:
        model = JobPost