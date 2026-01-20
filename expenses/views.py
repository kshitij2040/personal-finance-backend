"""
Expense views for CRUD operations
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get expense summary statistics"""
        total = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
        by_category = Expense.objects.values('category').annotate(
            total=Sum('amount')
        ).order_by('-total')
        
        return Response({
            'total_expenses': float(total),
            'by_category': list(by_category)
        })
    
    @action(detail=False, methods=['get'])
    def monthly(self, request):
        """Get monthly expense breakdown"""
        monthly_data = Expense.objects.annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            total=Sum('amount')
        ).order_by('month')
        
        return Response(list(monthly_data))
