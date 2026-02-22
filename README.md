# LLM Evaluator - Backend

Backend implementation for the LLM Evaluator system.

## Architecture

### Layer 1: Rubrics Management
- **Domain Selection**: Manage and select evaluation domains
- **Dynamic Rubric Builder**: Create and manage custom rubrics
- **Weight Configuration**: Configure weights for rubric consolidation

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy environment file:
```bash
cp .env.example .env
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Domain Selection (`/api/v1/domains`)

- `GET /api/v1/domains` - Get all domains (with optional filters: `category`, `search`)
- `GET /api/v1/domains/{domain_id}` - Get a specific domain
- `POST /api/v1/domains` - Create a new domain
- `PUT /api/v1/domains/{domain_id}` - Update a domain
- `DELETE /api/v1/domains/{domain_id}` - Delete a domain
- `GET /api/v1/domains/categories/list` - Get all available domain categories

**Available Categories**: general, coding, mathematics, reasoning, language, science, business, medical, legal, education, creative, technical, custom

### Dynamic Rubric Builder (`/api/v1/rubrics`)

- `GET /api/v1/rubrics` - Get all rubrics (with optional filters: `domain_id`, `rubric_type`, `evaluation_dimension`)
- `GET /api/v1/rubrics/{rubric_id}` - Get a specific rubric
- `POST /api/v1/rubrics` - Create a new rubric
- `PUT /api/v1/rubrics/{rubric_id}` - Update a rubric
- `DELETE /api/v1/rubrics/{rubric_id}` - Delete a rubric
- `GET /api/v1/rubrics/domain/{domain_id}` - Get all rubrics for a domain
- `GET /api/v1/rubrics/types/list` - Get all available rubric types
- `POST /api/v1/rubrics/build-custom` - Build a custom rubric from criteria

**Available Rubric Types**: accuracy, reasoning, code_quality, mathematical_correctness, clarity, completeness, relevance, coherence, factual_correctness, creativity, custom

**Evaluation Dimensions**: prompt_quality, response_quality, overall_quality

### Weight Configuration (`/api/v1/weight-configs`)

- `GET /api/v1/weight-configs` - Get all weight configurations (with optional filter: `domain_id`)
- `GET /api/v1/weight-configs/{config_id}` - Get a specific weight configuration
- `POST /api/v1/weight-configs` - Create a new weight configuration
- `PUT /api/v1/weight-configs/{config_id}` - Update a weight configuration
- `DELETE /api/v1/weight-configs/{config_id}` - Delete a weight configuration
- `GET /api/v1/weight-configs/domain/{domain_id}` - Get all weight configs for a domain
- `POST /api/v1/weight-configs/from-rubrics` - Create weight config from rubric IDs

**Normalization Methods**: weighted_average, weighted_sum, max, min, geometric_mean

## Example Usage

See `example_usage.py` for comprehensive examples of using the API.

Run examples:
```bash
python example_usage.py
```

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── domain.py          # Domain API endpoints
│   │       ├── rubric.py          # Rubric API endpoints
│   │       └── weight_config.py   # Weight config API endpoints
│   ├── models/
│   │   ├── domain.py              # Domain data model
│   │   ├── rubric.py              # Rubric data model
│   │   └── weight_config.py       # Weight config data model
│   ├── schemas/
│   │   ├── domain.py              # Domain API schemas
│   │   ├── rubric.py              # Rubric API schemas
│   │   └── weight_config.py       # Weight config API schemas
│   ├── services/
│   │   ├── domain_service.py      # Domain business logic
│   │   ├── rubric_service.py      # Rubric business logic
│   │   └── weight_config_service.py # Weight config business logic
│   └── main.py                    # FastAPI application
├── requirements.txt
├── README.md
└── example_usage.py
```

## Features

- ✅ Domain selection with predefined and custom categories
- ✅ Dynamic rubric builder with multiple criteria and weights
- ✅ Weight configuration for consolidating multiple rubrics
- ✅ Full CRUD operations for all entities
- ✅ Validation and error handling
- ✅ RESTful API with OpenAPI documentation
- ✅ Default data pre-loaded for quick start

