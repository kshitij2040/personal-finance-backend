import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';
import LoginForm from '../components/LoginForm';

/**
 * Login Page
 */
export default function Login() {
    return (
        <>
            <Head>
                <title>Login - AI Finance Pencil</title>
            </Head>

            <Header />

            <div className="container">
                <LoginForm />
            </div>

            <Footer />
        </>
    );
}
