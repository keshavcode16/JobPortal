from django.urls import path
from rest_framework import routers


app_name = "search"


from .views import SearchJobView

router = routers.DefaultRouter()
router.register("search", SearchJobView, basename="search-job")

urlpatterns = [
    path("search/", SearchJobView.as_view({"get": "list"}), name="job_search")
]
