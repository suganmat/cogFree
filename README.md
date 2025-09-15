# Meal Suggestor Backend

A modular Python backend API for meal suggestions powered by OpenRouter LLM integration.

## Features

- **Chat Interface**: RESTful API for chat interactions
- **Dietician AI**: Expert meal suggestions based on user preferences
- **OpenRouter Integration**: Flexible LLM model support
- **Modular Architecture**: Easy to extend with new features
- **Comprehensive Logging**: Structured logging with Loguru
- **Input Validation**: Pydantic-based request validation
- **Error Handling**: Robust error handling and responses

## Quick Start

### Prerequisites

- Python 3.8+
- OpenRouter API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd meal-suggestor-backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenRouter API key
```

5. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

### Interactive Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints

#### Health Check
```http
GET /api/chat/health
```

#### Generate Meal Suggestion
```http
POST /api/chat/suggest
Content-Type: application/json

{
  "message": "I want a healthy vegetarian meal for dinner",
  "session_id": "optional-session-id"
}
```

#### Get Configuration
```http
GET /api/chat/config
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | Required |
| `OPENROUTER_MODEL` | LLM model to use | `openai/gpt-3.5-turbo` |
| `OPENROUTER_BASE_URL` | OpenRouter API base URL | `https://openrouter.ai/api/v1` |
| `PORT` | Server port | `8000` |
| `DEBUG` | Debug mode | `false` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Project Structure

```
meal-suggestor-backend/
├── app/
│   ├── api/           # API endpoints
│   ├── core/          # Core configuration
│   ├── models/        # Pydantic models
│   ├── services/      # Business logic
│   └── utils/         # Utility functions
├── tests/             # Test files
├── logs/              # Log files
├── main.py            # Application entry point
├── requirements.txt   # Dependencies
└── README.md          # This file
```

## Development

### Running in Development Mode
```bash
python main.py
```

### Running with Uvicorn
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Code Formatting
```bash
black .
isort .
```

## Testing

```bash
pytest tests/
```

## Example Usage

### Using curl
```bash
# Health check
curl http://localhost:8000/api/chat/health

# Generate meal suggestion
curl -X POST http://localhost:8000/api/chat/suggest \
  -H "Content-Type: application/json" \
  -d '{"message": "I need a quick lunch for work"}'
```

### Using Python requests
```python
import requests

# Generate meal suggestion
response = requests.post(
    "http://localhost:8000/api/chat/suggest",
    json={"message": "I want a healthy breakfast"}
)
print(response.json())
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License
