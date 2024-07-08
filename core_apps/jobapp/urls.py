from django.urls import include, path
from rest_framework import routers
from core_apps.jobapp import  views 


app_name = "jobapp"

router = routers.DefaultRouter()



urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.home_view),
    path('auth/login', views.LoginPageView.as_view(), name='user_auth_view'),
    path('register/<str:user_type>', views.register_view, name='register_view'),
    path('mail/user/<int:user_id>', views.email_verification_view, name='email_verification_view'),
    path('employer/dashboard', views.EmployerDashboardView.as_view(), name='employer_dashboard_view'),
    path('employer/profile/<int:employer_id>', views.ProfileView.as_view(), name='profile_view'),
    path('jobs/<int:employer_id>', views.JobPostView.as_view(), name='job_view'),
    path('jobs/<int:employer_id>/<int:job_id>', views.JobPostView.as_view(), name='job_edit'),
    path('view_jobs/', views.JobListView.as_view(), name='job_list_view'),
    path('job_detail/<int:job_id>', views.UserJobView.as_view(), name='job_detail_view'),
    path('apply/<int:job_id>', views.ApplyJobView.as_view(), name='apply_job_view'),
    path('user/dashboard', views.UserDashboardView.as_view(), name='user_dashboard_view'),
    path('applied_jobs/', views.AppliedJobListView.as_view(), name='applied_job_list_view'),
    path('user/logout', views.logout, name='user_logout')
]


