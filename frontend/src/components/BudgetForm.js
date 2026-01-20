import { useState } from 'react';

/**
 * Budget Form Component for adding income/expenses
 */
export default function BudgetForm({ type, onSubmit }) {
    const fieldName = type === 'expense' ? 'category' : 'source';

    const [formData, setFormData] = useState({
        amount: '',
        [fieldName]: type === 'expense' ? 'food' : 'salary',
        description: '',
        date: new Date().toISOString().split('T')[0],
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(formData);
        setFormData({
            amount: '',
            [fieldName]: type === 'expense' ? 'food' : 'salary',
            description: '',
            date: new Date().toISOString().split('T')[0],
        });
    };

    const expenseCategories = [
        { value: 'food', label: 'Food & Dining' },
        { value: 'transport', label: 'Transportation' },
        { value: 'utilities', label: 'Utilities' },
        { value: 'entertainment', label: 'Entertainment' },
        { value: 'healthcare', label: 'Healthcare' },
        { value: 'shopping', label: 'Shopping' },
        { value: 'education', label: 'Education' },
        { value: 'other', label: 'Other' },
    ];

    const incomeSources = [
        { value: 'salary', label: 'Salary' },
        { value: 'freelance', label: 'Freelance' },
        { value: 'business', label: 'Business' },
        { value: 'investment', label: 'Investment' },
        { value: 'gift', label: 'Gift' },
        { value: 'other', label: 'Other' },
    ];

    const options = type === 'expense' ? expenseCategories : incomeSources;
    const label = type === 'expense' ? 'Category' : 'Source';

    return (
        <form onSubmit={handleSubmit} className="card">
            <h3>Add {type === 'expense' ? 'Expense' : 'Income'}</h3>

            <div className="form-group">
                <label className="form-label">Amount ($)</label>
                <input
                    type="number"
                    name="amount"
                    className="form-control"
                    value={formData.amount}
                    onChange={handleChange}
                    required
                    step="0.01"
                    min="0"
                />
            </div>

            <div className="form-group">
                <label className="form-label">{label}</label>
                <select
                    name={fieldName}
                    className="form-control"
                    value={formData[fieldName]}
                    onChange={handleChange}
                >
                    {options.map(opt => (
                        <option key={opt.value} value={opt.value}>{opt.label}</option>
                    ))}
                </select>
            </div>

            <div className="form-group">
                <label className="form-label">Description</label>
                <input
                    type="text"
                    name="description"
                    className="form-control"
                    value={formData.description}
                    onChange={handleChange}
                    placeholder="Optional description"
                />
            </div>

            <div className="form-group">
                <label className="form-label">Date</label>
                <input
                    type="date"
                    name="date"
                    className="form-control"
                    value={formData.date}
                    onChange={handleChange}
                    required
                />
            </div>

            <button type="submit" className="btn btn-primary">
                Add {type === 'expense' ? 'Expense' : 'Income'}
            </button>
        </form>
    );
}
