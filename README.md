# Pawn Shop Backend API

<p align="center">
  <a href="https://fastapi.tiangolo.com/" target="_blank">
    <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" width="200" alt="FastAPI Logo" />
  </a>
</p>

<p align="center">
  A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
</p>

<p align="center">
  <a href="https://hub.docker.com/" target="_blank"><img src="https://img.shields.io/badge/Docker-ready-blue" alt="Docker Ready" /></a>
  <a href="https://fastapi.tiangolo.com/" target="_blank"><img src="https://img.shields.io/badge/FastAPI-Docs-brightgreen" alt="FastAPI Docs" /></a>
  <a href="https://pypi.org/project/fastapi/" target="_blank"><img src="https://img.shields.io/badge/PyPI-Version-brightgreen" alt="PyPI Version" /></a>
  <a href="https://github.com/tiangolo/fastapi" target="_blank"><img src="https://img.shields.io/github/stars/tiangolo/fastapi?style=social" alt="GitHub Stars" /></a>
</p>

---

## 📦 Description

This is a robust backend API for a pawn shop management system built with FastAPI. The system provides comprehensive functionality for managing pawn shop operations, including client management, order processing, product inventory, and user authentication.

## 🚀 Features

- **Authentication & Authorization**
  - OAuth2 implementation for secure access
  - User management and role-based access control

- **Client Management**
  - Client registration and profile management
  - Client history tracking
  - Client relationship management

- **Pawn Operations**
  - Pawn item registration
  - Valuation management
  - Contract generation and management
  - Interest calculation

- **Order Processing**
  - Order creation and management
  - Transaction history
  - Payment processing

- **Product Management**
  - Inventory management
  - Product categorization
  - Product status tracking

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL (via SQLAlchemy)
- **Authentication:** OAuth2
- **Containerization:** Docker
- **API Documentation:** Swagger/OpenAPI

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Docker (recommended)
- pip (Python package manager)

### Docker Deployment (Recommended)

The easiest way to run the application is using Docker Compose, which includes a PostgreSQL database:

```bash
# 1. Clone the repository
git clone <repository-url>
cd pawn_shop_backend

# 2. Build and start containers
docker compose up --build
```

This will:
- Start a PostgreSQL database container
- Build and start the FastAPI application
- Set up all necessary environment variables automatically

The application will be available at:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Local Development

1. Create Virtual Environment
- For Windows
```bash
# Create environment
python -m venv env

# Activate environment
env\Scripts\activate
```
- For Mac/Linux
```bash
# Create environment
python3 -m venv venv

# Activate environment
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database:
```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE pawnshop;
CREATE USER pawnshop WITH PASSWORD 'pawnshop123';
GRANT ALL PRIVILEGES ON DATABASE pawnshop TO pawnshop;
\q
```

4. Set up environment variables (copy from env.example):
```bash
cp env.example .env
# Edit .env file with your configuration
```

5. Test database connection:
```bash
python test_db.py
```

6. Run the application:
```bash
uvicorn main:app --reload
```

## 🔐 Environment Variables

The application uses environment variables for configuration. These can be set in a `.env` file in the project root.

### Required Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes | - |
| `SECRET_KEY` | Secret key for JWT tokens | Yes | - |
| `ENVIRONMENT` | Environment (development/production) | No | development |
| `ALLOWED_ORIGINS` | CORS allowed origins (comma-separated) | No | http://localhost:3000 |
| `ALLOWED_HOSTS` | Trusted hosts (comma-separated) | No | localhost,127.0.0.1 |

### Database Configuration Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `POSTGRES_DB` | PostgreSQL database name | No | pawnshop |
| `POSTGRES_USER` | PostgreSQL username | No | pawnshop |
| `POSTGRES_PASSWORD` | PostgreSQL password | No | pawnshop123 |

### Docker Compose Environment Variables

When using Docker Compose, the application automatically reads environment variables from the `.env` file. The docker-compose.yaml file uses the `${VARIABLE_NAME:-default_value}` syntax to set environment variables with fallback defaults.

**Example .env file:**
```env
# Database Configuration
POSTGRES_DB=pawnshop
POSTGRES_USER=pawnshop
POSTGRES_PASSWORD=pawnshop123
DATABASE_URL=postgresql://pawnshop:pawnshop123@db:5432/pawnshop

# Security
SECRET_KEY=your-super-secret-key-here-change-this-in-production
ALGORITHM=HS256

# Token Configuration
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Environment
ENVIRONMENT=development

# CORS and Hosts
ALLOWED_ORIGINS=http://localhost:3000
ALLOWED_HOSTS=localhost,127.0.0.1

# Default Admin User
DEFAULT_ADMIN_NAME=Admin
DEFAULT_ADMIN_PHONE=069260405
DEFAULT_ADMIN_PASSWORD=M^bd4LC3^f~Z|iE?}
```

### Testing Environment Variables

You can test if your environment variables are loaded correctly:

```bash
# Test environment variable loading
python3 test_env.py

# Test database connection
python3 test_db.py

# Validate Docker Compose configuration
docker compose config
```

## 📚 API Documentation

Once the application is running, you can access:

- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/health`

## 🔧 Troubleshooting

### Common Issues

1. **Database Connection Error**: 
   - Ensure PostgreSQL is running
   - Check `DATABASE_URL` is correct
   - For Docker: Ensure the database container is running
   - Run `python test_db.py` to test connection

2. **CORS Errors**: 
   - Check `ALLOWED_ORIGINS` configuration
   - Ensure frontend URL is included in allowed origins

3. **Authentication Issues**: 
   - Verify `SECRET_KEY` is set correctly
   - Check token expiration settings

4. **Docker Issues**:
   - Ensure Docker and Docker Compose are installed
   - Check if ports 8000 and 5432 are available
   - Run `docker compose logs` to see detailed error messages

### Health Check

The application includes a health check endpoint at `/health` that returns:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected"
}
```

### Database Connection Testing

Use the included test script to verify database connectivity:
```bash
python test_db.py
```

## 🚀 Production Deployment Checklist

- [ ] Set strong `SECRET_KEY` for production
- [ ] Configure proper `ALLOWED_ORIGINS` for your frontend domain
- [ ] Set up proper `ALLOWED_HOSTS` for your domain
- [ ] Use strong database passwords
- [ ] Set `ENVIRONMENT=production`
- [ ] Configure SSL/TLS certificates
- [ ] Set up database backups
- [ ] Configure monitoring and logging
- [ ] Set up proper firewall rules
- [ ] Consider using a reverse proxy (nginx)
