/**
 * Header Component
 */
export default function Header() {
    return (
        <header style={styles.header}>
            <div className="container" style={styles.container}>
                <h1 style={styles.title}>💰 AI Finance Pencil</h1>
                <nav style={styles.nav}>
                    <a href="/" style={styles.link}>Home</a>
                    <a href="/dashboard" style={styles.link}>Dashboard</a>
                </nav>
            </div>
        </header>
    );
}

const styles = {
    header: {
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: '20px 0',
        marginBottom: '30px',
        boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
    },
    container: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
    },
    title: {
        color: 'white',
        fontSize: '28px',
        fontWeight: '700',
        margin: 0,
    },
    nav: {
        display: 'flex',
        gap: '20px',
    },
    link: {
        color: 'white',
        textDecoration: 'none',
        fontSize: '16px',
        fontWeight: '600',
        transition: 'opacity 0.3s ease',
    },
};
