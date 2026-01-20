"""
Income views for CRUD operations
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import Income
from .serializers import IncomeSerializer


class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get income summary statistics"""
        total = Income.objects.aggregate(total=Sum('amount'))['total'] or 0
        by_source = Income.objects.values('source').annotate(
            total=Sum('amount')
        ).order_by('-total')
        
        return Response({
            'total_income': float(total),
            'by_source': list(by_source)
        })
    
    @action(detail=False, methods=['get'])
    def monthly(self, request):
        """Get monthly income breakdown"""
        monthly_data = Income.objects.annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            total=Sum('amount')
        ).order_by('month')
        
        return Response(list(monthly_data))
