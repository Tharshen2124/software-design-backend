# Backend Setup Instructions

## Prerequisites

- Python 3.8+
- Supabase account

## Installation

### 1. Create & Activate Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root with the following variables:

```
FRONTEND_URL=your_frontend_url
BACKEND_URL=your_backend_url
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_REDIRECT_PATH=auth/callback/
DJANGO_SECRET_KEY=your_django_secret_key
SENDGRID_KEY=your_sendgrid_api_key
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Start Development Server

```bash
python manage.py runserver
```

The server will be accessible at: `http://localhost:8000`

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

## First-Time Setup Resources

If you're setting up for the first time, you may need to install:

- [Python](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## Troubleshooting

If you encounter any issues during setup, please check that all prerequisites are properly installed and environment variables are correctly configured.
