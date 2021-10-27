from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from students.views import CoursesViewSet, sample_view

router = DefaultRouter()
router.register("courses", CoursesViewSet, basename="courses")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include(router.urls)),
    path('api/v1/sample/', sample_view, name='sample'),
]
