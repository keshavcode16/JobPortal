from django.db import models
from core_apps.users.models import JobSeeker, Employer 
from core_apps.common.models import Skill, Qualification 
from django.db.models import Q





class JobPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    skills = models.ManyToManyField(Skill)
    slug = models.SlugField()
    experience_years = models.IntegerField(blank=True, null=True)
    experience_months = models.IntegerField(blank=True, null=True)
    created_by = models.ForeignKey(Employer, related_name="jobposts", db_index=True, on_delete=models.CASCADE)
    qualification = models.ManyToManyField(Qualification)
    vacancies = models.IntegerField(default=1)
    
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    status = models.BooleanField(u'Status', default=True)
    
    major_skill = models.ForeignKey(
        Skill,
        null=True,
        blank=True,
        related_name="major_skill",
        on_delete=models.CASCADE,
    )
    
    
    
    class Meta:
        verbose_name = "Job Post"
        ordering = ["-created_on"]

    def __unicode__(self):
        return self.title

    def get_similar_jobs(self):
        jobs = (
            JobPost.objects.filter(Q(skills__in=self.skills.all()))
            .exclude(pk=self.id)
            .distinct()
        )
        jobs = (
            jobs.filter(status=True)
        )
        return jobs

    def get_recommended_jobs(self):
        jobs = (
            JobPost.objects.filter(skills__in=self.skills.all())
            .exclude(pk=self.id)
            .distinct()
        )
        jobs = (
            jobs.filter(status=True)
        )
        return jobs

    def get_skills(self):
        return self.skills.filter(status=True)

    def get_qualification(self):
        return self.qalification.filter(status=True).order_by("name")




class JobApplication(models.Model):
    POST_STATUS = (
        ("Rejected", "Rejected"),
        ("Shortlisted", "Shortlisted"),
        ("Selected", "Selected"),
    )
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    user = models.ForeignKey(JobSeeker, null=True, blank=True, db_index=True, on_delete=models.CASCADE)
    status = models.CharField(choices=POST_STATUS, max_length=50)
    applied_on = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "Job Application"


