import { useState, useEffect } from 'react';
import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Dashboard from '../components/Dashboard';
import BudgetForm from '../components/BudgetForm';
import TransactionList from '../components/TransactionList';
import { expenseAPI, incomeAPI } from '../utils/api';

/**
 * Main Dashboard Page
 */
export default function DashboardPage() {
    const [expenses, setExpenses] = useState([]);
    const [income, setIncome] = useState([]);
    const [refreshKey, setRefreshKey] = useState(0);

    useEffect(() => {
        loadData();
    }, [refreshKey]);

    const loadData = async () => {
        try {
            const [expensesRes, incomeRes] = await Promise.all([
                expenseAPI.getAll(),
                incomeAPI.getAll(),
            ]);
            setExpenses(expensesRes.data.results || expensesRes.data || []);
            setIncome(incomeRes.data.results || incomeRes.data || []);
        } catch (error) {
            console.error('Error loading data:', error);
        }
    };

    const handleAddExpense = async (data) => {
        try {
            await expenseAPI.create(data);
            setRefreshKey(prev => prev + 1);
        } catch (error) {
            console.error('Error adding expense:', error);
            alert('Failed to add expense');
        }
    };

    const handleAddIncome = async (data) => {
        try {
            await incomeAPI.create(data);
            setRefreshKey(prev => prev + 1);
        } catch (error) {
            console.error('Error adding income:', error);
            alert('Failed to add income');
        }
    };

    const handleDeleteExpense = async (id) => {
        if (confirm('Are you sure you want to delete this expense?')) {
            try {
                await expenseAPI.delete(id);
                setRefreshKey(prev => prev + 1);
            } catch (error) {
                console.error('Error deleting expense:', error);
                alert('Failed to delete expense');
            }
        }
    };

    const handleDeleteIncome = async (id) => {
        if (confirm('Are you sure you want to delete this income?')) {
            try {
                await incomeAPI.delete(id);
                setRefreshKey(prev => prev + 1);
            } catch (error) {
                console.error('Error deleting income:', error);
                alert('Failed to delete income');
            }
        }
    };

    return (
        <>
            <Head>
                <title>Dashboard - AI Finance Pencil</title>
            </Head>

            <Header />

            <div className="container">
                <h1 style={{ color: 'white', marginBottom: '30px', fontSize: '36px' }}>
                    📊 Your Financial Dashboard
                </h1>

                {/* Dashboard Overview with Charts */}
                <Dashboard key={refreshKey} />

                {/* Add Transaction Forms */}
                <div className="grid grid-2" style={{ marginTop: '30px' }}>
                    <BudgetForm type="income" onSubmit={handleAddIncome} />
                    <BudgetForm type="expense" onSubmit={handleAddExpense} />
                </div>

                {/* Transaction Lists */}
                <div style={{ marginTop: '30px' }}>
                    <TransactionList
                        transactions={income.slice(0, 10)}
                        type="income"
                        onDelete={handleDeleteIncome}
                    />
                </div>

                <div style={{ marginTop: '20px' }}>
                    <TransactionList
                        transactions={expenses.slice(0, 10)}
                        type="expense"
                        onDelete={handleDeleteExpense}
                    />
                </div>
            </div>

            <Footer />
        </>
    );
}
