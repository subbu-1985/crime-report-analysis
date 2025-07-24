# Andhra Pradesh Crime Analytics Dashboard

<img width="1920" height="932" alt="demo" src="https://github.com/user-attachments/assets/40eed735-953d-43ee-ad2a-7ca277432dba" />

This project is a comprehensive crime analytics system for Andhra Pradesh, India. It consists of a backend API service, a frontend dashboard, and machine learning models for crime classification and analysis.

## Project Structure

- **backend/**: FastAPI backend service providing REST API endpoints for crime data, maps, and chatbot integration.
- **frontend/**: Web dashboard frontend built with HTML, CSS, and JavaScript to visualize crime analytics.
- **ml/**: Machine learning models and training scripts for crime classification.
- **docker-compose.yml**: Docker Compose configuration to run the backend and frontend services.
- **README.md**: Project documentation and instructions.

## Backend

The backend is built with FastAPI and provides APIs for crime data, map integration, and chatbot services. It uses PostgreSQL as the database and Alembic for database migrations.

### Key Features

- Real-time crime monitoring and analysis
- REST API endpoints for crime data, maps, and chatbot
- Database connection pooling and configuration
- CORS enabled for frontend integration
- Logging and health check endpoints

## Frontend

The frontend is a web dashboard that consumes the backend APIs to display crime analytics data visually. It includes interactive maps, charts, and chatbot interface.

## Machine Learning

The ML module contains scripts and pre-trained models for crime classification. It supports training new models and integrating them with the backend services.

## Setup and Running the Project

### Prerequisites

- Python 3.12+
- Node.js and npm (for frontend if needed)
- PostgreSQL database
- Docker and Docker Compose (optional, for containerized setup)

### Backend Setup

1. Navigate to the backend directory:

```bash
cd backend
```

2. Create and activate a Python virtual environment:

```bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Linux/macOS
```

3. Install the required Python packages:

```bash
pip install -r requirements.txt
pip install pydantic-settings
```

4. Configure environment variables in a `.env` file in the backend directory (refer to `backend/config.py` for required variables).

5. Run database migrations using Alembic:

```bash
alembic upgrade head
```

6. Start the backend server:

```bash
uvicorn app:app --reload
```

The backend API will be available at `http://127.0.0.1:8000`.

### Frontend Setup

Open `frontend/index.html` in a web browser or serve it using a static file server.

### Machine Learning

The ML models are located in `ml/models/`. You can train new models using the scripts in `ml/train_model.py`.

## Additional Notes

- Ensure the PostgreSQL database is running and accessible with the configured credentials.
- The backend supports CORS for the frontend origins specified in the configuration.
- Use the health check endpoint `/health` to verify the backend status.

## Contact

For any issues or contributions, please contact the project maintainer.

---
