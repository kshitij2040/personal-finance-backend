"""
Financial Advisor Agent using Pydantic AI
Provides personalized budget insights, savings recommendations, and investment advice
"""
from typing import List
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.gemini import GeminiModel
from django.db.models import Sum, Count
from decimal import Decimal
from expenses.models import Expense
from income.models import Income
from django.conf import settings


# ===== Pydantic Models for Structured Outputs =====

class SpendingAnalysis(BaseModel):
    """Analysis of spending in a specific category"""
    category: str = Field(description="The spending category")
    amount_spent: float = Field(description="Total amount spent in this category")
    percentage_of_income: float = Field(description="What % of income this represents")
    concern_level: str = Field(description="low, medium, or high")
    insight: str = Field(description="Brief insight about this spending")


class SavingRecommendation(BaseModel):
    """Recommendation for saving money in a category"""
    category: str = Field(description="Category to reduce spending")
    current_spending: float = Field(description="Current monthly spending")
    recommended_spending: float = Field(description="Recommended spending amount")
    potential_monthly_savings: float = Field(description="How much you could save")
    actionable_tips: List[str] = Field(description="3-5 specific tips to reduce spending")


class InvestmentSuggestion(BaseModel):
    """Suggested investment based on savings"""
    investment_type: str = Field(description="Type of investment (e.g., Emergency Fund, Index Fund)")
    amount_to_invest: float = Field(description="Suggested amount to invest")
    priority: str = Field(description="low, medium, or high priority")
    reason: str = Field(description="Why this investment is recommended")
    risk_level: str = Field(description="low, medium, or high risk")


class FinancialInsights(BaseModel):
    """Complete financial insights report"""
    total_income: float = Field(description="Total income")
    total_expenses: float = Field(description="Total expenses") 
    current_savings_rate: float = Field(description="Current savings rate as percentage")
    financial_health_score: int = Field(description="Overall score from 0-100")
    
    spending_analysis: List[SpendingAnalysis] = Field(description="Analysis of spending patterns")
    top_overspending_categories: List[str] = Field(description="Categories where spending is excessive")
    
    savings_recommendations: List[SavingRecommendation] = Field(description="How to save money")
    total_potential_savings: float = Field(description="Total monthly amount that could be saved")
    
    investment_suggestions: List[InvestmentSuggestion] = Field(description="Investment recommendations")
    
    overall_summary: str = Field(description="2-3 sentence summary of financial situation")
    key_action_items: List[str] = Field(description="3-5 immediate actions to take")


# ===== Agent Tools =====

def get_spending_by_category() -> dict:
    """Get total spending grouped by category"""
    expenses = Expense.objects.values('category').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')
    
    return {
        item['category']: {
            'total': float(item['total'] or 0),
            'count': item['count']
        }
        for item in expenses
    }


def get_income_summary() -> dict:
    """Get total income and breakdown by source"""
    total_income = Income.objects.aggregate(total=Sum('amount'))['total'] or 0
    income_by_source = Income.objects.values('source').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    return {
        'total': float(total_income),
        'by_source': {item['source']: float(item['total']) for item in income_by_source}
    }


def get_total_expenses() -> float:
    """Get total expenses"""
    total = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
    return float(total)


def get_top_individual_expenses(limit: int = 5) -> list:
    """Get the top individual expense transactions"""
    expenses = Expense.objects.order_by('-amount')[:limit]
    return [
        {
            'amount': float(exp.amount),
            'category': exp.category,
            'description': exp.description,
            'date': exp.date.isoformat()
        }
        for exp in expenses
    ]


# ===== Pydantic AI Agent =====

# System prompt for the financial advisor
SYSTEM_PROMPT = """You are an expert financial advisor specializing in personal budgeting and savings.

Your role is to:
1. Analyze spending patterns and identify areas of overspending
2. Provide specific, actionable recommendations to save money
3. Suggest appropriate investment strategies based on the user's financial situation
4. Calculate a financial health score (0-100) based on:
   - Savings rate (higher is better)
   - Spending balance across categories
   - Emergency fund status
   - Debt situation

Be direct, practical, and encouraging. Focus on realistic tips that the user can implement immediately.
When analyzing spending:
- Compare to typical % of income for each category
- Flag if any category exceeds 30% of income as HIGH concern
- Flag 20-30% as MEDIUM concern
- Below 20% is LOW concern

For savings recommendations:
- Suggest realistic reductions (not extreme cuts)
- Provide 3-5 specific actionable tips for each category
- Calculate potential monthly savings

For investments:
- Emergency fund should be the first priority (3-6 months expenses)
- Then suggest low-cost index funds or retirement accounts
- Match risk level to their savings capacity
"""


def create_financial_advisor_agent():
    """Create and configure the financial advisor agent"""
    # Create Gemini model with API key
    model = GeminiModel('gemini-1.5-flash', api_key=settings.GEMINI_API_KEY)
    
    # Create agent with the model
    agent = Agent(
        model,
        result_type=FinancialInsights,
        system_prompt=SYSTEM_PROMPT,
    )
    
    # Register tools
    @agent.tool
    async def analyze_spending() -> dict:
        """Get current spending breakdown by category"""
        return get_spending_by_category()

    @agent.tool  
    async def get_income() -> dict:
        """Get total income and sources"""
        return get_income_summary()

    @agent.tool
    async def get_expense_total() -> float:
        """Get total amount spent"""
        return get_total_expenses()

    @agent.tool
    async def get_biggest_expenses() -> list:
        """Get the top 5 largest individual expenses"""
        return get_top_individual_expenses()
    
    return agent


# ===== Main Function to Run Agent =====

async def get_financial_insights() -> FinancialInsights:
    """
    Run the financial advisor agent and get structured insights
    """
    # Create the agent
    agent = create_financial_advisor_agent()
    
    prompt = """Analyze my current budget and provide comprehensive financial insights.

Please:
1. Analyze my spending patterns across all categories
2. Identify where I'm overspending
3. Give me specific recommendations on how to save money
4. Suggest where I should invest my savings
5. Calculate my financial health score
6. Provide key action items I should take immediately

Use the available tools to get my actual budget data, then provide detailed insights."""

    result = await agent.run(prompt)
    
    return result.data
