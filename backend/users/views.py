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

# Import Gemini API
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


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
    """Get AI-powered budget insights using Google Gemini with structured JSON output"""
    
    # Step 1: Check if Gemini is available
    if not GEMINI_AVAILABLE:
        return Response({
            'error': 'Google Generative AI library not installed',
            'tip': 'Install with: pip install google-generativeai',
            'step': 'library_check'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    # Step 2: Check API key
    if not settings.GEMINI_API_KEY:
        return Response({
            'error': 'Gemini API key not configured',
            'tip': 'Add GEMINI_API_KEY to your .env file',
            'step': 'api_key_check'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    try:
        # Step 3: Get financial data
        try:
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
        except Exception as e:
            return Response({
                'error': f'Database query failed: {str(e)}',
                'step': 'database_query',
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Step 4: Create prompt
        try:
            prompt = f"""You are a financial advisor. Analyze this budget and provide insights in JSON.

Budget: Income ${total_income}, Expenses ${total_expenses}, Savings {savings_rate:.1f}%

Return ONLY this JSON structure (no markdown, no extra text):
{{
  "total_income": {total_income},
  "total_expenses": {total_expenses},
  "current_savings_rate": {savings_rate:.1f},
  "financial_health_score": 75,
  "spending_analysis": [{{"category": "food", "amount_spent": 100, "percentage_of_income": 5, "concern_level": "low", "insight": "Good"}}],
  "top_overspending_categories": [],
  "savings_recommendations": [{{"category": "food", "current_spending": 100, "recommended_spending": 80, "potential_monthly_savings": 20, "actionable_tips": ["Cook at home"]}}],
  "total_potential_savings": 50,
  "investment_suggestions": [{{"investment_type": "Emergency Fund", "amount_to_invest": 200, "priority": "high", "reason": "Build emergency fund", "risk_level": "low"}}],
  "overall_summary": "Your finances are on track. Keep saving!",
  "key_action_items": ["Continue current savings plan", "Build emergency fund"]
}}

Use the actual budget data above. Return valid JSON only."""
        except Exception as e:
            return Response({
                'error': f'Prompt creation failed: {str(e)}',
                'step': 'prompt_creation',
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Step 5: Call Gemini API
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            
            # Try to list available models
            try:
                models = genai.list_models()
                available = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
                print(f"Available Gemini models: {available}")
                
                # Use the first available model
                if available:
                    model_name = available[0].replace('models/', '')
                    print(f"Using model: {model_name}")
                    model = genai.GenerativeModel(model_name)
                else:
                    # Fallback to trying common names
                    model = genai.GenerativeModel('gemini-pro')
            except Exception as list_error:
                print(f"Could not list models: {list_error}")
                # Try common model names
                model = genai.GenerativeModel('gemini-pro')
            
            # Generate insights
            response = model.generate_content(prompt)
            insights_text = response.text.strip()
            
            # If we got here, AI worked! No need for mock data
            print("✅ Successfully generated AI insights!")
            
        except Exception as e:
            print(f"Gemini API failed, using mock data: {str(e)}")
            # Return mock data as fallback
            insights_text = json.dumps({
                "total_income": float(total_income),
                "total_expenses": float(total_expenses),
                "current_savings_rate": savings_rate,
                "financial_health_score": 75,
                "spending_analysis": [
                    {
                        "category": cat['category'],
                        "amount_spent": float(cat['amount']),
                        "percentage_of_income": cat['percentage'],
                        "concern_level": "high" if cat['percentage'] > 30 else "medium" if cat['percentage'] > 20 else "low",
                        "insight": f"You're spending {cat['percentage']:.1f}% of your income on {cat['category']}"
                    }
                    for cat in expense_breakdown[:3]
                ] if expense_breakdown else [],
                "top_overspending_categories": [cat['category'] for cat in expense_breakdown[:2]] if expense_breakdown else [],
                "savings_recommendations": [
                    {
                        "category": expense_breakdown[0]['category'] if expense_breakdown else "general",
                        "current_spending": expense_breakdown[0]['amount'] if expense_breakdown else 0,
                        "recommended_spending": (expense_breakdown[0]['amount'] * 0.8) if expense_breakdown else 0,
                        "potential_monthly_savings": (expense_breakdown[0]['amount'] * 0.2) if expense_breakdown else 0,
                        "actionable_tips": [
                            "Track your spending daily",
                            "Set a monthly budget",
                            "Look for cheaper alternatives",
                            "Reduce unnecessary purchases"
                        ]
                    }
                ] if expense_breakdown else [],
                "total_potential_savings": (float(total_expenses) * 0.15) if total_expenses > 0 else 0,
                "investment_suggestions": [
                    {
                        "investment_type": "Emergency Fund",
                        "amount_to_invest": balance * 0.5 if balance > 0 else 100,
                        "priority": "high",
                        "reason": "Build 3-6 months of expenses for financial security",
                        "risk_level": "low"
                    }
                ],
                "overall_summary": f"You're currently saving {savings_rate:.1f}% of your income. {'Great job!' if savings_rate > 20 else 'Try to increase your savings rate.'} (Note: AI unavailable - {str(e)})",
                "key_action_items": [
                    "Review your largest expense categories",
                    "Set up automatic savings transfers",
                    "Create a monthly budget plan"
                ]
            })
        
        # Step 6: Parse JSON
        try:
            # Remove markdown code blocks if present
            if insights_text.startswith('```json'):
                insights_text = insights_text.split('```json')[1]
            if insights_text.startswith('```'):
                insights_text = insights_text.split('```')[1]
            if insights_text.endswith('```'):
                insights_text = insights_text.rsplit('```', 1)[0]
            insights_text = insights_text.strip()
            
            insights_data = json.loads(insights_text)
        except json.JSONDecodeError as e:
            return Response({
                'error': f'JSON parsing failed: {str(e)}',
                'raw_response': insights_text[:500],
                'step': 'json_parsing',
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                'error': f'Unexpected parsing error: {str(e)}',
                'step': 'json_parsing',
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Success!
        return Response({
            'success': True,
            'insights': insights_data
        })
        
    except Exception as e:
        import traceback
        return Response({
            'error': f'Unexpected error: {str(e)}',
            'traceback': traceback.format_exc()[:1000],
            'step': 'unknown',
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
