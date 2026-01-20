"""
User views including AI insights powered by pydantic-ai and Google Gemini
"""
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from expenses.models import Expense
from income.models import Income
from django.conf import settings
import json
from users.agents.financial_advisor import get_financial_insights


@api_view(['GET'])
def get_budget_overview(request):
    """Get overall budget statistics"""
    total_income = Income.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
    balance = float(total_income) - float(total_expenses)
    
    # Get category breakdowns
    expense_by_category = list(Expense.objects.values('category').annotate(
        total=Sum('amount')
    ).order_by('-total'))
    
    income_by_source = list(Income.objects.values('source').annotate(
        total=Sum('amount')
    ).order_by('-total'))
    
    return Response({
        'total_income': float(total_income),
        'total_expenses': float(total_expenses),
        'balance': balance,
        'expense_by_category': expense_by_category,
        'income_by_source': income_by_source,
    })


@api_view(['POST'])
def get_ai_insights(request):
    """Get AI-powered budget insights using pydantic-ai with Google Gemini"""
    
    try:
        # Get financial data
        total_income = Income.objects.aggregate(total=Sum('amount'))['total'] or 0
        total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
        balance = float(total_income) - float(total_expenses)
        savings_rate = ((float(total_income) - float(total_expenses)) / float(total_income) * 100) if total_income > 0 else 0
        
        expense_by_category = list(Expense.objects.values('category').annotate(
            total=Sum('amount')
        ).order_by('-total'))
        
        # Format expense data
        expense_breakdown = []
        for item in expense_by_category:
            pct = (float(item['total']) / float(total_income) * 100) if total_income > 0 else 0
            expense_breakdown.append({
                'category': item['category'],
                'amount': float(item['total']),
                'percentage': round(pct, 1)
            })
        
        # Prepare budget data for AI
        budget_data = {
            'total_income': float(total_income),
            'total_expenses': float(total_expenses),
            'balance': balance,
            'savings_rate': savings_rate,
            'expense_breakdown': expense_breakdown
        }
        
        # Call pydantic-ai agent
        insights = get_financial_insights(budget_data)
        
        # Convert pydantic model to dict
        insights_dict = insights.model_dump()
        
        return Response({
            'success': True,
            'insights': insights_dict
        })
        
    except Exception as e:
        import traceback
        print(f"Error in get_ai_insights: {str(e)}")
        print(traceback.format_exc())
        
        # Return mock data on error
        return Response({
            'success': False,
            'error': str(e),
            'insights': {
                "total_income": float(total_income) if 'total_income' in locals() else 0,
                "total_expenses": float(total_expenses) if 'total_expenses' in locals() else 0,
                "current_savings_rate": savings_rate if 'savings_rate' in locals() else 0,
                "financial_health_score": 75,
                "spending_analysis": [],
                "top_overspending_categories": [],
                "savings_recommendations": [],
                "total_potential_savings": 0,
                "investment_suggestions": [{
                    "investment_type": "Emergency Fund",
                    "amount_to_invest": 100,
                    "priority": "high",
                    "reason": "Build emergency fund",
                    "risk_level": "low"
                }],
                "overall_summary": f"AI service temporarily unavailable: {str(e)}",
                "key_action_items": ["Review your budget", "Track expenses"]
            }
        }, status=status.HTTP_200_OK)
