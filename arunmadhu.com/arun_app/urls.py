from django.urls import path
from . import views
from arun_app.views import project_views
from arun_app.views import home_views

urlpatterns = [
    path('', home_views.home, name='home'),
    path('home/', home_views.home, name='home'),
    path('project01/',project_views.project01, name='project01'),
    path('project02/',project_views.project02, name='project02'),
    path('project03/',project_views.project03, name='project03'),
    path('project04/',project_views.project04, name='project04'),
    path('project05/',project_views.project05, name='project05'),
    path('project06/',project_views.project06, name='project06'),
    path('project07/',project_views.project07, name='project07'),
    path('project08/',project_views.project08, name='project08'),
    path('project09/',project_views.project09, name='project09'),
]
