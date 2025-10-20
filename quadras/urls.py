from django.urls import path
from . import views

app_name = 'quadras'

urlpatterns = [
    path('<int:pk>/', views.CourtTemplateView.as_view(), name='home')
]