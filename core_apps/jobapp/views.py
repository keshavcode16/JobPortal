from django.conf import settings
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Avg, Count
from notifications.models import Notification
from rest_framework import generics, mixins, status, viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import JobPost, JobApplication
from core_apps.users import forms as user_forms
from core_apps.users.models import User, Employer, JobSeeker
from .renderers import (JobPostJSONRenderer)
from .serializers import (JobPostSerializer)
from core_apps.profiles.models import Profile
import traceback
from django.shortcuts import get_object_or_404, redirect, render
from collections import defaultdict 
from django.views.generic import View
from django.views.generic.list import ListView 
from django.contrib.auth import login, authenticate, user_logged_in, get_user_model
from django.contrib import messages
from django.urls import reverse
from .utils import get_all_form_errors
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateJobPostForm
from django.db.models import Q
from django.contrib.auth import logout as auth_logout



import logging
logger = logging.getLogger("loggers")


def home_view(request):
    context = {}
    return render(request, "public/home.html", context)


def user_auth_view(request, user_type):
    context = {}
    return render(request, "auth.html", context)



def job_list_view(request, model_slug):
    context = {}
    return render(request, "product_list.html", context)


class LargeResultsSetPagination(PageNumberPagination):
    """
    Set pagination results settings
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10



class LoginPageView(View):
    template_name = 'public/auth.html'
    form_class = user_forms.AuthForm
    
    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                if user.user_type == "EMPLOYER" and user.is_verified:
                    return redirect('jobapp:employer_dashboard_view')
                elif (user.user_type == 'EMPLOYER'  or user.user_type == 'JOB_SEEKER') and not user.is_verified:
                    return redirect(reverse('jobapp:email_verification_view', kwargs={'user_id': user.pk}))
                elif user.user_type == 'JOB_SEEKER'  and not user.is_verified:
                    return redirect('jobapp:user_dashboard_view')
                return redirect('jobapp:user_dashboard_view')
            else:
                messages.error(request, 'Username and Password are matching.')
                
        message = 'Login failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})



class EmployerDashboardView(LoginRequiredMixin, View):
    template_name = 'employer/dashboard.html'
    login_url = '/auth/login'
    
    def get(self, request):
        context = {}
        logger.info(f'request.user {request.user}')
        employer_object = Employer.objects.filter(id=request.user.pk).first()
        if employer_object is not None and request.user.is_authenticated:
            context['employer_object'] = employer_object 
            context['full_name'] = employer_object.get_full_name() 
            context['total_job_count'] = employer_object.get_total_job_counts()
            context['total_job_applicants'] = employer_object.get_total_job_applicants()
        return render(request, self.template_name, context=context)
    


class UserJobView(LoginRequiredMixin, View):
    template_name = 'job_seeker/job_detail.html'
    # form_class = user_forms.ApplyJobFom
    login_url = '/auth/login'
    
    def get(self, request, job_id):
        context = {}
        logger.info(f'request.user {request.user}')
        context['allowed_to_apply']  = True
        user_object = JobSeeker.objects.filter(id=request.user.pk).first()
        if user_object is not None and request.user.is_authenticated:
            context['user_object'] = user_object 
            context['full_name'] = user_object.get_full_name() 
            
        job_object = JobPost.objects.filter(id=job_id).first()  
        if job_object is not None:
            applied_job_app_object = JobApplication.objects.filter(job_post=job_object,user=user_object).first()
            if applied_job_app_object is not None:
                context['allowed_to_apply']  = False
            context['job'] = job_object 
        return render(request, self.template_name, context=context)

class ApplyJobView(LoginRequiredMixin, View):
    template_name = 'job_seeker/job_detail.html'
    # form_class = user_forms.ApplyJobFom
    login_url = '/auth/login'
    
    def get(self, request, job_id):
        context = {}
        context['allowed_to_apply']  = True
        logger.info(f'request.user {request.user}')
        user_object = JobSeeker.objects.filter(id=request.user.pk).first()
        if user_object is not None and request.user.is_authenticated:
            context['user_object'] = user_object 
            context['full_name'] = user_object.get_full_name()
        try:
            job_object = JobPost.objects.filter(id=job_id).first()  
            applied_job_app_object = JobApplication.objects.filter(job_post=job_object,user=user_object).first()
            if job_object is not None and user_object.user_type=='JOB_SEEKER' and applied_job_app_object is None:
                context['job'] = job_object
                applied_job_app_object = JobApplication.objects.create(job_post=job_object,user=user_object)
                messages.success(request, "Job has been applied successfully")
            else:
                context['allowed_to_apply']  = False
                messages.success(request, "You  have already applied jobs")
        except Exception as err:
            messages.error(request, f"Error in applying job {str(err)}")
        return render(request, self.template_name, context=context)
        


class UserDashboardView(LoginRequiredMixin, View):
    template_name = 'job_seeker/dashboard.html'
    form_class = user_forms.AuthForm
    login_url = '/auth/login'
    
    def get(self, request):
        context = {}
        logger.info(f'request.user {request.user}')
        user_object = JobSeeker.objects.filter(id=request.user.pk).first()
        if user_object is not None and request.user.is_authenticated:
            context['user_object'] = user_object 
            context['full_name'] = user_object.get_full_name() 
        
        # Handle search query
        search_query = request.GET.get('q')
        if search_query:
            job_posts = JobPost.objects.filter(title__icontains=search_query)
            context['job_posts'] = job_posts
        else:
            # If no search query, display all job posts
            context['job_posts'] = JobPost.objects.all()
            
            
        return render(request, self.template_name, context=context)


class ProfileView(LoginRequiredMixin, View):
    template_name = 'employer/profile.html'
    form_class = user_forms.UpdateEmployerForm
    login_url = '/auth/login'
    
    def get(self, request, employer_id):
        context = {}
        employer = get_object_or_404(Employer, id=employer_id)
        profile_form = self.form_class(instance=employer)
        context['profile_form'] = profile_form 
        context['employer_object'] = employer 
        context['full_name'] = employer.get_full_name() 
        return render(request, self.template_name, context=context)
    
    def post(self, request, employer_id):
        employer = get_object_or_404(Employer, id=employer_id)
        if request.method == 'POST':
            form = self.form_class(request.POST, instance=employer)
            
            if form.is_valid():
                form.save()
                messages.success(request, "Employer account updated successfully.") 
                return redirect(reverse('jobapp:profile_view', kwargs={'employer_id': employer_id})) 
            else:
                if '__all__' in form.errors.as_data():
                    messages.error(request, ''.join(form.errors.as_data()['__all__'][0]))
                else:
                    err_messages = get_all_form_errors(form)
                    messages.error(request, err_messages)
        message = 'Login failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})



class JobPostView(LoginRequiredMixin, View):
    template_name = 'employer/job_posts.html'
    form_class = CreateJobPostForm
    login_url = '/auth/login'
    
    def get(self, request, employer_id):
        context = {}
        employer = get_object_or_404(Employer, id=employer_id)
        job_form = self.form_class()
        context['form'] = job_form 
        context['employer_object'] = employer 
        context['full_name'] = employer.get_full_name() 
        return render(request, self.template_name, context=context)
    
    def post(self, request, employer_id):
        context = {}
        form = self.form_class()
        employer = get_object_or_404(Employer, id=employer_id)
        context['employer_object'] = employer 
        context['full_name'] = employer.get_full_name() 
        if request.method == 'POST':
            form = self.form_class(request.POST, created_by=employer)
            form.instance.created_by = employer
            if form.is_valid():
                form.save()
                messages.success(request, "Jobs created successfully.") 
                return redirect(reverse('jobapp:profile_view', kwargs={'employer_id': employer_id})) 
            else:
                logger.error(f'Got Error form.errors {form.errors}')
                if '__all__' in form.errors.as_data():
                    messages.error(request, ''.join(form.errors.as_data()['__all__'][0]))
                else:
                    err_messages = get_all_form_errors(form)
                    messages.error(request, err_messages) 
        context['form'] = form
        return render(request, self.template_name, context=context)



class JobListView(LoginRequiredMixin, ListView): 
    model = JobPost 
    template_name = 'employer/jobs.html'
    login_url = '/auth/login'
    context_object_name = 'object_list'
    paginate_by = 10  # Adjust as needed
   
    def get_queryset(self, *args, **kwargs): 
        qs = super().get_queryset(*args, **kwargs)
        if self.request.user is not None and self.request.user.user_type == 'EMPLOYER':
            qs = qs.filter(created_by__id=self.request.user.pk)
        # Handle search
        search_query = self.request.GET.get('q')
        if search_query:
            qs = qs.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        qs = qs.order_by("-id") 
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.user_type == 'EMPLOYER':
            employer_object = Employer.objects.filter(id=self.request.user.pk).first()
            context['employer_object'] = employer_object
            context['full_name'] = employer_object.get_full_name()
        return context


class AppliedJobListView(LoginRequiredMixin, ListView): 
    model = JobApplication
    template_name = 'employer/job_application.html'
    login_url = '/auth/login'
    context_object_name = 'object_list'
    paginate_by = 10  # Adjust as needed
   
    def get_queryset(self, *args, **kwargs): 
        qs = super().get_queryset(*args, **kwargs)
        if self.request.user is not None and self.request.user.user_type == 'EMPLOYER':
            qs = qs.filter(job_post__created_by__id=self.request.user.pk)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.user_type == 'EMPLOYER':
            employer_object = Employer.objects.filter(id=self.request.user.pk).first()
            context['employer_object'] = employer_object
            context['full_name'] = employer_object.get_full_name()
        return context




def register_view(request, user_type):
    meta_text = ""
    if (user_type == 'employer'):
        meta_text = "Register As Job Employer"
        form = user_forms.CreateEmployerForm() 
    elif (user_type == 'user'):
        meta_text = "Register As Job Seeker"
        form = user_forms.CreateJobSeekerForm() 

    if request.method == 'POST':
        resSuccessMsg = ""
        if (user_type == 'employer'):
            resSuccessMsg = "Employer has been registered successfully!"
            form = user_forms.CreateEmployerForm(request.POST)
        elif (user_type == 'user'):
            resSuccessMsg = "User has been registered successfully!"
            form = user_forms.CreateJobSeekerForm(request.POST)

        if form.is_valid():
            form.save()
            user_obj = User.objects.filter(id=form.instance.pk).first()
            user_obj.set_password(form.instance.password)
            user_obj.save()
            messages.success(request, resSuccessMsg)  
            user_id = form.instance.pk 
            return redirect(reverse('jobapp:email_verification_view', kwargs={'user_id': user_id})) 
        else:
            logger.error(f'Got Register Error form.errors {form.errors}')
            if '__all__' in form.errors.as_data():
                messages.error(request, ''.join(form.errors.as_data()['__all__'][0]))
            else:
                err_messages = get_all_form_errors(form)
                messages.error(request, err_messages)

    return render(request, "public/register.html", {"form": form, 'meta_text': meta_text})


def email_verification_view(request, user_id):
    raiseErrr, meta_text = True, ''
    try:
        user_obj = None
        user_obj = User.objects.get(id=user_id)
    except User.DoesNotExist:
        pass
    if user_obj is not None and not user_obj.is_verified:
        resMessage = f"Please verify your mail before login sent you mail at {user_obj.email}"
        messages.success(request, resMessage) 
    elif user_obj is not None and user_obj.is_verified:
        resMessage = f"Your email has been verified already."
        messages.success(request, resMessage) 
    else:
        messages.error(request,"User not found")
    return render(request, "public/email_verification.html", {'meta_text': meta_text, 'raiseErrr': raiseErrr})



def logout(request):
    auth_logout(request)
    return redirect('jobapp:user_auth_view')