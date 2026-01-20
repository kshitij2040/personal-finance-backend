"""
Income admin configuration
"""
from django.contrib import admin
from .models import Income


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['source', 'amount', 'date', 'description']
    list_filter = ['source', 'date']
    search_fields = ['description']
    date_hierarchy = 'date'
