import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';

/**
 * Landing Page
 */
export default function Home() {
    return (
        <>
            <Head>
                <title>AI Finance Pencil - Smart Budget Tracker</title>
            </Head>

            <Header />

            <div className="container">
                <div className="card" style={{ textAlign: 'center', maxWidth: '800px', margin: '0 auto' }}>
                    <h1 style={{ fontSize: '48px', marginBottom: '20px', color: '#6366f1' }}>
                        Welcome to AI Finance Pencil 💰
                    </h1>
                    <p style={{ fontSize: '20px', color: '#6b7280', marginBottom: '30px' }}>
                        Your smart budget tracking companion powered by Google Gemini AI
                    </p>

                    <div style={{ marginBottom: '40px' }}>
                        <h2 style={{ color: '#1f2937', marginBottom: '20px' }}>Features</h2>
                        <div className="grid grid-3">
                            <div style={featureCard}>
                                <div style={{ fontSize: '48px', marginBottom: '10px' }}>📊</div>
                                <h3>Track Finances</h3>
                                <p style={{ color: '#6b7280' }}>Monitor income and expenses with ease</p>
                            </div>
                            <div style={featureCard}>
                                <div style={{ fontSize: '48px', marginBottom: '10px' }}>📈</div>
                                <h3>Visual Reports</h3>
                                <p style={{ color: '#6b7280' }}>Beautiful charts and analytics</p>
                            </div>
                            <div style={featureCard}>
                                <div style={{ fontSize: '48px', marginBottom: '10px' }}>🤖</div>
                                <h3>AI Insights</h3>
                                <p style={{ color: '#6b7280' }}>Smart budgeting tips from Gemini AI</p>
                            </div>
                        </div>
                    </div>

                    <a href="/dashboard" className="btn btn-primary" style={{ fontSize: '20px', padding: '16px 40px' }}>
                        Get Started →
                    </a>
                </div>
            </div>

            <Footer />
        </>
    );
}

const featureCard = {
    padding: '20px',
    background: 'linear-gradient(135deg, #f9fafb, #e5e7eb)',
    borderRadius: '12px',
};
