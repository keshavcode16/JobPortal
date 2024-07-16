from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import JobPost
from core_apps.search.documents import JobPostDocument
from datetime import date
from django_elasticsearch_dsl.registries import registry


@receiver(post_save, sender=JobPost)
def update_jobpost(sender, instance=None, created=False, **kwargs):
    registry.update(instance)
    # instance.save()
    # JobPostDocument(title=instance.title, description=instance.description, skills=[skill.name for skill in instance.skills.all()], slug=instance.slug,experience_years=instance.experience_years,experience_months=instance.experience_months, qualification=instance.qualification.name, vacancies=instance.vacancies, created_on=instance.created_on.date(), modified_on=(instance.modified_on.date() if instance.modified_on else date.today()), status=instance.status).save()

@receiver(post_delete, sender=JobPost)
def delete_jobpost(sender, instance=None, **kwargs):
    # JobPostDocument.get(id=instance.id).delete()
    registry.delete(instance)


