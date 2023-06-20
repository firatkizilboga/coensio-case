from django.urls import path
from .views import (
    CreateExamView,
    GetResultsView
)

urlpatterns = [
    path('exam/', CreateExamView.as_view(), name='create-exam'),
    path('getResults/', GetResultsView.as_view(), name='get-results'),
]
