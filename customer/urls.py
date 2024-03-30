from django.urls import path
from .views import Identify

urlpatterns = [
    path('identify/', Identify.as_view()),
]
