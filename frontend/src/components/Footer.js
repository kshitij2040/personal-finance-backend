/**
 * Footer Component
 */
export default function Footer() {
    return (
        <footer style={styles.footer}>
            <div className="container">
                <p style={styles.text}>
                    © 2026 AI Finance Pencil | Powered by Google Gemini AI
                </p>
            </div>
        </footer>
    );
}

const styles = {
    footer: {
        background: 'rgba(255, 255, 255, 0.1)',
        padding: '20px 0',
        marginTop: '50px',
        textAlign: 'center',
    },
    text: {
        color: 'white',
        fontSize: '14px',
        margin: 0,
    },
};
