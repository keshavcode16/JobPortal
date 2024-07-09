from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import JobPost
from .documents import JobPostDocument
from datetime import date


@receiver(post_save, sender=JobPost)
def index_jobpost(sender, instance, **kwargs):
    instance.save()
    JobPostDocument(title=instance.title, description=instance.description, skills=[skill.name for skill in instance.skills.all()], slug=instance.slug,experience_years=instance.experience_years,experience_months=instance.experience_months, qualification=instance.qualification.name, vacancies=instance.vacancies, created_on=instance.created_on.date(), modified_on=(instance.modified_on.date() if instance.modified_on else date.today()), status=instance.status).save()

@receiver(post_delete, sender=JobPost)
def delete_jobpost(sender, instance, **kwargs):
    JobPostDocument.get(id=instance.id).delete()

