"""
User views including AI insights powered by Google Gemini
"""
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from expenses.models import Expense
from income.models import Income
from django.conf import settings
import json
import google.generativeai as genai


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
    """Get AI-powered budget insights using Google Gemini API"""
    
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
        
        # Configure Gemini
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Create prompt
        prompt = f"""You are a financial advisor. Analyze this budget and provide insights in JSON format.

Budget Data:
- Total Income: ${total_income}
- Total Expenses: ${total_expenses}
- Current Savings Rate: {savings_rate:.1f}%
- Expense Breakdown: {json.dumps(expense_breakdown)}

Return ONLY a valid JSON object (no markdown, no code blocks) with this exact structure:
{{
  "total_income": {total_income},
  "total_expenses": {total_expenses},
  "current_savings_rate": {savings_rate:.1f},
  "financial_health_score": 85,
  "spending_analysis": [
    {{
      "category": "Food",
      "amount_spent": 500,
      "percentage_of_income": 10,
      "concern_level": "low",
      "insight": "Your food spending is well-managed"
    }}
  ],
  "top_overspending_categories": ["Entertainment", "Dining"],
  "savings_recommendations": [
    {{
      "category": "Entertainment",
      "current_spending": 300,
      "recommended_spending": 200,
      "potential_monthly_savings": 100,
      "actionable_tips": ["Set a monthly entertainment budget", "Look for free activities"]
    }}
  ],
  "total_potential_savings": 200,
  "investment_suggestions": [
    {{
      "investment_type": "Emergency Fund",
      "amount_to_invest": 500,
      "priority": "high",
      "reason": "Build 3-6 months emergency fund",
      "risk_level": "low"
    }}
  ],
  "overall_summary": "Your financial health is good. Focus on building emergency savings.",
  "key_action_items": ["Build emergency fund", "Track spending", "Review subscriptions"]
}}

Analyze the actual budget data above and provide personalized insights."""

        # Call Gemini API
        response = model.generate_content(prompt)
        insights_text = response.text.strip()
        
        # Clean markdown formatting
        if insights_text.startswith('```json'):
            insights_text = insights_text.split('```json')[1]
        if insights_text.startswith('```'):
            insights_text = insights_text.split('```')[1]
        if insights_text.endswith('```'):
            insights_text = insights_text.rsplit('```', 1)[0]
        insights_text = insights_text.strip()
        
        # Parse JSON
        insights_data = json.loads(insights_text)
        
        return Response({
            'success': True,
            'insights': insights_data
        })
        
    except Exception as e:
        import traceback
        print(f"Error in get_ai_insights: {str(e)}")
        print(traceback.format_exc())
        
        # Return error with mock data
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
                "overall_summary": f"AI temporarily unavailable: {str(e)}",
                "key_action_items": ["Review your budget", "Track expenses"]
            }
        }, status=status.HTTP_200_OK)
