# Blog API

A modern, high-performance RESTful API for blogging, built with FastAPI, SQLAlchemy, and Alembic.

## Features
- User registration and authentication (JWT)
- Blog CRUD operations
- Commenting system
- Request logging middleware
- Database migrations with Alembic
- Automatic API docs (Swagger UI)

## Setup

1. **Clone the repository:**
	```bash
	git clone <your-repo-url>
	cd Blog
	```
2. **Activate the virtual environment:**
	```bash
	poetry shell
	```
3. **Install dependencies:**
	```bash
	poetry install
	```
4. **Run migrations:**
	```bash
	alembic upgrade head
	```
5. **Start the server:**
	```bash
	poetry run uvicorn app.main:app --reload
	```

## Usage
- Access API docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Register, login, and use JWT tokens for authenticated requests
- Create, update, and delete blogs and comments

## Project Structure
```
app/
  api/         # API endpoints
  core/        # Config and core logic
  db/          # Database setup
  middleware/  # Custom middlewares
  models/      # SQLAlchemy models
  schemas/     # Pydantic schemas
migrations/    # Alembic migration scripts
README.md      # Project documentation
```

## Environment Variables
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT signing key

## License
MIT
