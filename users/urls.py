"""
User URL configuration
"""
from django.urls import path
from .views import get_budget_overview, get_ai_insights

urlpatterns = [
    path('overview/', get_budget_overview, name='budget-overview'),
    path('ai-insights/', get_ai_insights, name='ai-insights'),
]
