from django.urls import path
from . import views

app_name = 'patterns'
 
urlpatterns = [
    path('', views.index, name='index'),
    path('pattern/<int:pattern_id>/', views.pattern_detail, name='detail'),
    path('api/patterns/', views.api_patterns, name='api_patterns'),
] 