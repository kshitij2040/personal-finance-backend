# AI Finance Pencil - Setup Guide

Welcome to AI Finance Pencil! This guide will help you set up and run your budget tracker application.

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (for Django backend)
- **Node.js 16+** (for Next.js frontend)
- **pip** (Python package manager)
- **npm** (Node.js package manager)

### Backend Setup (Django)

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment (recommended):**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy `.env.example` to `.env`
   - Edit `.env` and add your configuration (optional for now)

5. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional, for admin panel):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the Django development server:**
   ```bash
   python manage.py runserver
   ```

   The backend API will be available at `http://localhost:8000`

### Frontend Setup (Next.js)

1. **Open a new terminal and navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables (optional):**
   - Copy `.env.local.example` to `.env.local`
   - Default API URL is already configured

4. **Start the Next.js development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

## 🎯 Using the Application

1. **Open your browser** and go to `http://localhost:3000`
2. **Click "Get Started"** to access the dashboard
3. **Add your first income or expense** using the forms
4. **View your financial overview** with charts and statistics
5. **Get AI insights** by clicking the "Get AI Insights" button

## 🤖 Setting Up Google Gemini AI (Optional)

To enable AI-powered budget insights:

1. **Get a free API key:**
   - Visit [Google AI Studio](https://ai.google.dev)
   - Sign in with your Google account
   - Create a new API key

2. **Add the API key to backend:**
   - Edit `backend/.env`
   - Add: `GEMINI_API_KEY=your-api-key-here`
   - Restart the Django server

3. **Test AI insights:**
   - Go to the dashboard
   - Click "Get AI Insights" button
   - Gemini will analyze your budget and provide tips!

## 📊 Features

- ✅ **Income Tracking** - Record all income sources
- ✅ **Expense Tracking** - Track spending by category
- ✅ **Visual Charts** - Pie charts and bar graphs
- ✅ **Budget Overview** - See total income, expenses, and balance
- ✅ **AI Insights** - Smart budgeting tips from Gemini AI
- ✅ **REST API** - Full CRUD operations
- ✅ **Responsive Design** - Works on all devices

## 🗄️ Database

The application uses **SQLite** by default, which requires no setup. Your data is stored in `backend/db.sqlite3`.

### Migrating to Supabase (Optional)

If you want to use Supabase instead:

1. Create a free account at [supabase.com](https://supabase.com)
2. Create a new project
3. Get your database credentials from Project Settings → Database
4. Update `backend/config/settings/common.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'your_supabase_host',
           'PORT': '5432',
       }
   }
   ```
5. Install PostgreSQL adapter: `pip install psycopg2-binary`
6. Run migrations again: `python manage.py migrate`

## 🛠️ API Endpoints

### Expenses
- `GET /api/expenses/` - List all expenses
- `POST /api/expenses/` - Create expense
- `GET /api/expenses/{id}/` - Get expense details
- `PUT /api/expenses/{id}/` - Update expense
- `DELETE /api/expenses/{id}/` - Delete expense
- `GET /api/expenses/summary/` - Get expense summary
- `GET /api/expenses/monthly/` - Get monthly breakdown

### Income
- `GET /api/income/` - List all income
- `POST /api/income/` - Create income
- `GET /api/income/{id}/` - Get income details
- `PUT /api/income/{id}/` - Update income
- `DELETE /api/income/{id}/` - Delete income
- `GET /api/income/summary/` - Get income summary
- `GET /api/income/monthly/` - Get monthly breakdown

### Budget & AI
- `GET /api/users/overview/` - Get budget overview
- `POST /api/users/ai-insights/` - Get AI insights

## 🐛 Troubleshooting

### Backend won't start
- Make sure Python 3.8+ is installed: `python --version`
- Ensure virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`
- Run migrations: `python manage.py migrate`

### Frontend won't start
- Make sure Node.js 16+ is installed: `node --version`
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Clear Next.js cache: `rm -rf .next`

### CORS errors
- Make sure backend is running on port 8000
- Check `backend/config/settings/common.py` CORS settings

### AI insights not working
- Verify `GEMINI_API_KEY` is set in `backend/.env`
- Check console for error messages
- Ensure `google-generativeai` is installed

## 📝 Next Steps

- Add user authentication
- Create mobile app version
- Add data export features
- Implement budget goals
- Add recurring transactions
- Create financial reports

## 💡 Tips

- Use the Django admin panel at `http://localhost:8000/admin` for data management
- Add sample data to test charts and visualizations
- Check the browser console for debugging information
- AI insights work best with at least a week of data

## 🤝 Support

For issues or questions:
- Check the troubleshooting section
- Review the API documentation
- Ensure both backend and frontend servers are running

Enjoy tracking your finances with AI Finance Pencil! 💰✨
