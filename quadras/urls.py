from django.urls import path
from . import views

app_name = 'quadras'

urlpatterns = [
    path('', views.CourtsListView.as_view(), name='list'),
    path('<int:pk>/', views.CourtScheduleDetailView.as_view(), name='detail'),
]