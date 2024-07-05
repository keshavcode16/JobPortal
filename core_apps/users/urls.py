from django.urls import path
app_name = 'users'
from core_apps.users import views



urlpatterns = [
    path('activate/<uidb64>/<token>', views.Activate.as_view(), name="activate"),
]
