/**
 * Transaction List Component
 */
export default function TransactionList({ transactions, type, onDelete }) {
    if (!transactions || transactions.length === 0) {
        return (
            <div className="card">
                <h3>{type === 'expense' ? 'Recent Expenses' : 'Recent Income'}</h3>
                <p style={{ color: '#6b7280', textAlign: 'center', padding: '20px' }}>
                    No {type === 'expense' ? 'expenses' : 'income'} yet. Add your first entry!
                </p>
            </div>
        );
    }

    return (
        <div className="card">
            <h3>{type === 'expense' ? 'Recent Expenses' : 'Recent Income'}</h3>
            <div style={{ overflowX: 'auto' }}>
                <table className="table">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>{type === 'expense' ? 'Category' : 'Source'}</th>
                            <th>Amount</th>
                            <th>Description</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {transactions.map((transaction) => (
                            <tr key={transaction.id}>
                                <td>{new Date(transaction.date).toLocaleDateString()}</td>
                                <td style={{ textTransform: 'capitalize' }}>
                                    {transaction.category || transaction.source}
                                </td>
                                <td style={{ fontWeight: '600', color: type === 'expense' ? '#ef4444' : '#10b981' }}>
                                    ${parseFloat(transaction.amount).toFixed(2)}
                                </td>
                                <td>{transaction.description || '-'}</td>
                                <td>
                                    <button
                                        onClick={() => onDelete(transaction.id)}
                                        className="btn btn-danger"
                                        style={{ padding: '6px 12px', fontSize: '14px' }}
                                    >
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
