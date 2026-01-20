import { useEffect, useState } from 'react';
import { Chart as ChartJS, ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Pie, Bar } from 'react-chartjs-2';
import { budgetAPI } from '../utils/api';

ChartJS.register(ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

/**
 * Dashboard Component with Charts and AI Insights
 */
export default function Dashboard() {
    const [overview, setOverview] = useState(null);
    const [aiInsights, setAIInsights] = useState(null);
    const [loading, setLoading] = useState(true);
    const [loadingAI, setLoadingAI] = useState(false);

    useEffect(() => {
        loadOverview();
    }, []);

    const loadOverview = async () => {
        try {
            const response = await budgetAPI.getOverview();
            setOverview(response.data);
        } catch (error) {
            console.error('Error loading overview:', error);
        } finally {
            setLoading(false);
        }
    };

    const getAIInsights = async () => {
        setLoadingAI(true);
        try {
            const response = await budgetAPI.getAIInsights();
            if (response.data.success && response.data.insights) {
                setAIInsights(response.data.insights);
            } else {
                console.error('AI response error:', response.data);
                alert(response.data.error || 'Failed to load AI insights');
            }
        } catch (error) {
            console.error('AI Insights Error:', error);
            console.error('Error response data:', error.response?.data);
            alert(`Failed to load AI insights. Error: ${error.response?.data?.error || error.message}`);
        } finally {
            setLoadingAI(false);
        }
    };

    if (loading) {
        return <div className="spinner"></div>;
    }

    if (!overview) {
        return <div className="card"><p>No data available</p></div>;
    }

    // Expense Chart Data
    const expenseChartData = {
        labels: overview.expense_by_category.map(item =>
            item.category.charAt(0).toUpperCase() + item.category.slice(1)
        ),
        datasets: [{
            label: 'Expenses by Category',
            data: overview.expense_by_category.map(item => item.total),
            backgroundColor: [
                '#ef4444', '#f59e0b', '#10b981', '#3b82f6',
                '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'
            ],
        }],
    };

    // Income Chart Data
    const incomeChartData = {
        labels: overview.income_by_source.map(item =>
            item.source.charAt(0).toUpperCase() + item.source.slice(1)
        ),
        datasets: [{
            label: 'Income by Source',
            data: overview.income_by_source.map(item => item.total),
            backgroundColor: '#10b981',
        }],
    };

    const getConcernColor = (level) => {
        if (level === 'high') return '#ef4444';
        if (level === 'medium') return '#f59e0b';
        return '#10b981';
    };

    const getConcernIcon = (level) => {
        if (level === 'high') return '●';
        if (level === 'medium') return '●';
        return '●';
    };

    return (
        <div>
            {/* Stats Cards */}
            <div className="grid grid-3" style={{ marginBottom: '30px' }}>
                <div className="stat-card" style={{ background: 'linear-gradient(135deg, #10b981, #059669)' }}>
                    <div className="stat-value">${overview.total_income.toFixed(2)}</div>
                    <div className="stat-label">Total Income</div>
                </div>
                <div className="stat-card" style={{ background: 'linear-gradient(135deg, #ef4444, #dc2626)' }}>
                    <div className="stat-value">${overview.total_expenses.toFixed(2)}</div>
                    <div className="stat-label">Total Expenses</div>
                </div>
                <div className="stat-card" style={{
                    background: overview.balance >= 0
                        ? 'linear-gradient(135deg, #6366f1, #4f46e5)'
                        : 'linear-gradient(135deg, #f59e0b, #d97706)'
                }}>
                    <div className="stat-value">${overview.balance.toFixed(2)}</div>
                    <div className="stat-label">Balance</div>
                </div>
            </div>

            {/* Charts */}
            <div className="grid grid-2" style={{ marginBottom: '30px' }}>
                <div className="card">
                    <h3>Expenses by Category</h3>
                    {overview.expense_by_category.length > 0 ? (
                        <Pie data={expenseChartData} />
                    ) : (
                        <p style={{ textAlign: 'center', color: '#6b7280' }}>No expense data</p>
                    )}
                </div>
                <div className="card">
                    <h3>Income by Source</h3>
                    {overview.income_by_source.length > 0 ? (
                        <Bar data={incomeChartData} />
                    ) : (
                        <p style={{ textAlign: 'center', color: '#6b7280' }}>No income data</p>
                    )}
                </div>
            </div>

            {/* AI Insights */}
            <div className="card">
                <h3>🤖 AI Financial Advisor Insights</h3>
                {!aiInsights ? (
                    <button
                        onClick={getAIInsights}
                        className="btn btn-primary"
                        disabled={loadingAI}
                    >
                        {loadingAI ? 'Analyzing your budget...' : 'Get Personalized Insights'}
                    </button>
                ) : (
                    <div>
                        {/* Financial Health Score */}
                        <div style={{
                            background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                            color: 'white',
                            padding: '20px',
                            borderRadius: '12px',
                            marginBottom: '20px',
                            textAlign: 'center'
                        }}>
                            <div style={{ fontSize: '48px', fontWeight: '700' }}>{aiInsights.financial_health_score}/100</div>
                            <div style={{ fontSize: '18px', opacity: 0.9 }}>Financial Health Score</div>
                            <div style={{ fontSize: '14px', marginTop: '10px' }}>
                                Savings Rate: {aiInsights.current_savings_rate.toFixed(1)}%
                            </div>
                        </div>

                        {/* Overall Summary */}
                        <div style={{ background: '#f9fafb', padding: '20px', borderRadius: '8px', marginBottom: '20px' }}>
                            <h4 style={{ marginBottom: '10px' }}>Summary</h4>
                            <p style={{ lineHeight: '1.6', marginBottom: '15px' }}>{aiInsights.overall_summary}</p>

                            <h4 style={{ marginBottom: '10px' }}>Key Action Items</h4>
                            <ul style={{ paddingLeft: '20px', lineHeight: '1.8' }}>
                                {aiInsights.key_action_items.map((item, idx) => (
                                    <li key={idx}>{item}</li>
                                ))}
                            </ul>
                        </div>

                        {/* Spending Analysis */}
                        {aiInsights.spending_analysis && aiInsights.spending_analysis.length > 0 && (
                            <div style={{ marginBottom: '20px' }}>
                                <h4 style={{ marginBottom: '15px' }}>Spending Analysis</h4>
                                <div className="grid grid-2">
                                    {aiInsights.spending_analysis.map((analysis, idx) => (
                                        <div key={idx} style={{
                                            border: `2px solid ${getConcernColor(analysis.concern_level)}`,
                                            borderRadius: '8px',
                                            padding: '15px',
                                            marginBottom: '10px'
                                        }}>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                                                <strong style={{ textTransform: 'capitalize' }}>{analysis.category}</strong>
                                                <span>{getConcernIcon(analysis.concern_level)} {analysis.concern_level.toUpperCase()}</span>
                                            </div>
                                            <div style={{ fontSize: '24px', fontWeight: '700', color: '#ef4444', marginBottom: '5px' }}>
                                                ${analysis.amount_spent.toFixed(2)}
                                            </div>
                                            <div style={{ fontSize: '14px', color: '#6b7280', marginBottom: '10px' }}>
                                                {analysis.percentage_of_income.toFixed(1)}% of income
                                            </div>
                                            <p style={{ fontSize: '14px', lineHeight: '1.5' }}>{analysis.insight}</p>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Savings Recommendations */}
                        {aiInsights.savings_recommendations && aiInsights.savings_recommendations.length > 0 && (
                            <div style={{ marginBottom: '20px' }}>
                                <h4 style={{ marginBottom: '15px' }}>Savings Recommendations</h4>
                                <div style={{ background: '#10b981', color: 'white', padding: '15px', borderRadius: '8px', marginBottom: '15px', textAlign: 'center' }}>
                                    <div style={{ fontSize: '28px', fontWeight: '700' }}>
                                        ${aiInsights.total_potential_savings.toFixed(2)}/month
                                    </div>
                                    <div>Total Potential Savings</div>
                                </div>

                                {aiInsights.savings_recommendations.map((rec, idx) => (
                                    <div key={idx} style={{ background: '#f9fafb', padding: '20px', borderRadius: '8px', marginBottom: '15px' }}>
                                        <h5 style={{ textTransform: 'capitalize', marginBottom: '10px' }}>{rec.category}</h5>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '15px' }}>
                                            <div>
                                                <div style={{ fontSize: '14px', color: '#6b7280' }}>Current</div>
                                                <div style={{ fontSize: '20px', fontWeight: '600', color: '#ef4444' }}>
                                                    ${rec.current_spending.toFixed(2)}
                                                </div>
                                            </div>
                                            <div>
                                                <div style={{ fontSize: '14px', color: '#6b7280' }}>Recommended</div>
                                                <div style={{ fontSize: '20px', fontWeight: '600', color: '#10b981' }}>
                                                    ${rec.recommended_spending.toFixed(2)}
                                                </div>
                                            </div>
                                            <div>
                                                <div style={{ fontSize: '14px', color: '#6b7280' }}>Save</div>
                                                <div style={{ fontSize: '20px', fontWeight: '600', color: '#6366f1' }}>
                                                    ${rec.potential_monthly_savings.toFixed(2)}
                                                </div>
                                            </div>
                                        </div>
                                        <div style={{ borderTop: '1px solid #e5e7eb', paddingTop: '10px' }}>
                                            <strong style={{ fontSize: '14px' }}>Tips:</strong>
                                            <ul style={{ paddingLeft: '20px', marginTop: '8px', lineHeight: '1.8' }}>
                                                {rec.actionable_tips.map((tip, tipIdx) => (
                                                    <li key={tipIdx} style={{ fontSize: '14px' }}>{tip}</li>
                                                ))}
                                            </ul>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}

                        {/* Investment Suggestions */}
                        {aiInsights.investment_suggestions && aiInsights.investment_suggestions.length > 0 && (
                            <div style={{ marginBottom: '20px' }}>
                                <h4 style={{ marginBottom: '15px' }}>Investment Suggestions</h4>
                                {aiInsights.investment_suggestions.map((inv, idx) => (
                                    <div key={idx} style={{
                                        background: inv.priority === 'high' ? '#fef3c7' : '#f9fafb',
                                        padding: '20px',
                                        borderRadius: '8px',
                                        marginBottom: '10px',
                                        border: inv.priority === 'high' ? '2px solid #f59e0b' : 'none'
                                    }}>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '10px' }}>
                                            <div>
                                                <h5 style={{ marginBottom: '5px' }}>{inv.investment_type}</h5>
                                                <div style={{ fontSize: '14px', color: '#6b7280' }}>
                                                    Risk: <strong style={{ textTransform: 'uppercase' }}>{inv.risk_level}</strong> |
                                                    Priority: <strong style={{ textTransform: 'uppercase' }}>{inv.priority}</strong>
                                                </div>
                                            </div>
                                            <div style={{ fontSize: '24px', fontWeight: '700', color: '#6366f1' }}>
                                                ${Number(inv.amount_to_invest).toFixed(2)}
                                            </div>
                                        </div>
                                        <p style={{ fontSize: '14px', lineHeight: '1.6' }}>{inv.reason}</p>
                                    </div>
                                ))}
                            </div>
                        )}

                        <button
                            onClick={() => setAIInsights(null)}
                            className="btn btn-primary"
                            style={{ marginTop: '10px' }}
                        >
                            Get New Insights
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}
