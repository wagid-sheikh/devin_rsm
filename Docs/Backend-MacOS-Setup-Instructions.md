# TSV-RSM Backend Setup Instructions for macOS

This guide will walk you through setting up the TSV-RSM backend authentication system on your MacBook.

## Prerequisites

- macOS (any recent version)
- Homebrew package manager
- Git

## Step 1: Install Homebrew (if not already installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## Step 2: Install Required Software

### Install PostgreSQL 14+

```bash
brew install postgresql@14
brew services start postgresql@14
```

Add PostgreSQL to your PATH:
```bash
echo 'export PATH="/opt/homebrew/opt/postgresql@14/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Install Redis

```bash
brew install redis
brew services start redis
```

### Install Python 3.11+ (using pyenv)

```bash
# Install pyenv if not already installed
brew install pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc

# Install Python 3.12
pyenv install 3.12.8
pyenv global 3.12.8
```

### Install Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## Step 3: Clone the Repository

```bash
cd ~/repos  # or wherever you keep your projects
git clone https://github.com/wagid-sheikh/devin_rsm.git
cd devin_rsm/backend
```

## Step 4: Set Up PostgreSQL Database

Create the database and set up the postgres user:

```bash
# Connect to PostgreSQL
psql postgres

# In the PostgreSQL prompt, run:
CREATE DATABASE tsv_rsm_dev;
ALTER USER <your-mac-username> WITH PASSWORD 'postgres';
\q
```

**Note:** On macOS with Homebrew PostgreSQL, the default user is your Mac username, not 'postgres'. You may need to adjust the DATABASE_URL in your .env file accordingly.

## Step 5: Configure Environment Variables

Create a `.env` file in the backend directory:

```bash
cd ~/repos/devin_rsm/backend
cp .env.example .env
```

Edit the `.env` file with your preferred text editor:

```bash
# Database - adjust username if needed
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/tsv_rsm_dev

# Security
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS - use JSON array format
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# Redis
REDIS_URL=redis://localhost:6379/0

# Environment
ENVIRONMENT=development
```

## Step 6: Install Python Dependencies

**Important: Fix bcrypt/passlib compatibility issue first**

There's a known compatibility issue between passlib 1.7.4 and bcrypt 4.x+. You need to pin bcrypt to version 3.2.2:

```bash
cd ~/repos/devin_rsm/backend

# Edit pyproject.toml to add bcrypt version constraint
# Add this line after the passlib line in [tool.poetry.dependencies] section:
# bcrypt = "3.2.2"

# For quick fix, use this command:
sed -i '' '/passlib = {extras = \["bcrypt"\], version = "^1.7.4"}/a\
bcrypt = "3.2.2"' pyproject.toml

# Now install dependencies
poetry install
```

**Note:** If the sed command doesn't work on your system, manually edit `pyproject.toml` and add `bcrypt = "3.2.2"` on a new line right after the passlib dependency in the `[tool.poetry.dependencies]` section.

## Step 7: Run Database Migrations

```bash
poetry run alembic upgrade head
```

This creates the `users` table in your database.

## Step 8: Create Test User

Create a file `create_test_user.py` in the backend directory with this content:

```python
import asyncio
import uuid
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.core.security import get_password_hash

async def create_test_user():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.email == "wagid.sheikh@gmail.com")
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            print("Test user already exists!")
            return
        
        user = User(
            id=uuid.uuid4(),
            email="wagid.sheikh@gmail.com",
            password_hash=get_password_hash("Timbak2t#"),
            first_name="Wagid",
            last_name="Sheikh",
            status="active"
        )
        session.add(user)
        await session.commit()
        print(f"Test user created: {user.email}")

if __name__ == "__main__":
    asyncio.run(create_test_user())
```

Run the script:

```bash
poetry run python create_test_user.py
```

## Step 9: Start the FastAPI Server

```bash
poetry run uvicorn app.main:app --reload
```

The server will start on `http://localhost:8000`

## Step 10: Test the Authentication System

### Check Health Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Database ready check
curl http://localhost:8000/ready
```

### Test Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "wagid.sheikh@gmail.com", "password": "Timbak2t#"}'
```

Expected response:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### View API Documentation

Open your browser and visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Troubleshooting

### PostgreSQL Connection Issues

If you get connection errors, check that PostgreSQL is running:
```bash
brew services list | grep postgresql
```

If it's not running:
```bash
brew services start postgresql@14
```

### Redis Connection Issues

Check Redis is running:
```bash
brew services list | grep redis
```

If it's not running:
```bash
brew services start redis
```

### Database User Issues

On macOS, Homebrew PostgreSQL creates a user with your Mac username by default. You may need to:

1. Check your username:
```bash
whoami
```

2. Update DATABASE_URL in .env to use your actual username:
```
DATABASE_URL=postgresql+asyncpg://yourusername:password@localhost:5432/tsv_rsm_dev
```

3. Or create a 'postgres' superuser:
```bash
psql postgres -c "CREATE USER postgres WITH SUPERUSER PASSWORD 'postgres';"
```

### Port Already in Use

If port 8000 is already in use:
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9

# Or use a different port
poetry run uvicorn app.main:app --reload --port 8001
```

### bcrypt/passlib Compatibility Error

If you see an error like `error reading bcrypt version` or `AttributeError: module 'bcrypt' has no attribute '__about__'`:

1. Make sure you added the bcrypt version constraint to pyproject.toml:
```toml
bcrypt = "3.2.2"
```

2. Update the lock file and reinstall:
```bash
poetry lock --no-update
poetry install
```

This pins bcrypt to version 3.2.2 which is compatible with passlib 1.7.4.

## Next Steps

Now that your authentication system is set up, you can:
1. Test token refresh functionality with your refresh token
2. Test logout/token revocation
3. Implement additional protected endpoints like `/api/v1/auth/me`
4. Continue with frontend development

## Test User Credentials

- Email: `wagid.sheikh@gmail.com`
- Password: `Timbak2t#`

## API Endpoints Currently Implemented

- `POST /api/v1/auth/login` - Login and get tokens
- `POST /api/v1/auth/refresh` - Refresh access token using refresh token
- `POST /api/v1/auth/logout` - Logout and revoke tokens

## Additional Test Commands

### Test Token Refresh
```bash
# First login to get tokens
RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "wagid.sheikh@gmail.com", "password": "Timbak2t#"}')

# Extract refresh token
REFRESH_TOKEN=$(echo $RESPONSE | jq -r .refresh_token)

# Use refresh token to get new access token
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d "{\"refresh_token\": \"$REFRESH_TOKEN\"}"
```

### Test Logout and Token Revocation
```bash
# Logout with refresh token
curl -X POST http://localhost:8000/api/v1/auth/logout \
  -H "Content-Type: application/json" \
  -d "{\"refresh_token\": \"$REFRESH_TOKEN\"}"

# Try to use the revoked token (should fail)
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d "{\"refresh_token\": \"$REFRESH_TOKEN\"}"
```
