## Python Quick Start with `venv`
#development/python

### 1. Create and Activate

```bash
cd your-project-folder
python -m venv venv
touch main.py
```

**Activate:**

- **Windows:** `venv\Scripts\activate`  
- **macOS/Linux:** `source venv/bin/activate`

You'll see `(venv)` in your terminal prompt when it's active.

### 2. Install Packages

```bash
pip install dotenv devtools pydantic-ai logfire openai supabase
```

### 3. Save Dependencies

```bash
pip freeze > requirements.txt
```

### 4. Setting Up Tests

```bash
# Install pytest and coverage tools
pip install pytest pytest-cov

# Create test directory structure
mkdir -p tests
touch tests/__init__.py
touch tests/conftest.py
```

**Basic Test File Structure:**

```python
# tests/test_example.py
def test_simple():
    assert 1 + 1 == 2
```

**Run Tests:**

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=.

# Run specific test file
pytest tests/test_example.py
```

**Create pytest.ini:**

```ini
[pytest]
testpaths = tests src
python_files = test_*.py
python_classes = Test*
python_functions = test_*
# Optional: recursively search for tests in all directories
norecursedirs = .* venv build dist
```

**Alternative Directory Structure Options:**

```bash
# For specific nested test directories, you can run:
pytest src/insight/tests/

# Or use pattern matching:
pytest --ignore=src/legacy/ src/
```

### 5. Deactivate

```bash
deactivate
```

### 6. Install from `requirements.txt`

```bash
pip install -r requirements.txt
```

### Tips

- Always activate `venv` before working
- Add `venv/` to `.gitignore`
- Keep `requirements.txt` updated
- You can name your env: `python -m venv myenv`
- Upgrade pip: `python -m pip install --upgrade pip`
- When you get SSL certificate validation errors during pip operations (like 'NoneType' object has no attribute 'get'), the most reliable solution is to reinstall pip using the official installer:
```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py ;python get-pip.py ; rm get-pip.py
```

## Typical Project Structure

```
my-ai-api/
├── venv/                       # Virtual environment (excluded from git)
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configuration settings
│   ├── dependencies.py         # FastAPI dependencies
│   │
│   ├── agents/                 # Pydantic AI agents
│   │   ├── __init__.py
│   │   ├── chat_agent.py       # Chat/conversation agent
│   │   ├── analysis_agent.py   # Data analysis agent
│   │   └── summary_agent.py    # Text summarization agent
│   │
│   ├── api/                    # API route handlers
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py         # Chat endpoints
│   │   │   ├── analysis.py     # Analysis endpoints
│   │   │   └── health.py       # Health check endpoints
│   │   └── dependencies.py
│   │
│   ├── models/                 # Pydantic models
│   │   ├── __init__.py
│   │   ├── requests.py         # Request models
│   │   ├── responses.py        # Response models
│   │   └── schemas.py          # Shared schemas
│   │
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── ai_service.py       # AI interaction service
│   │   ├── data_service.py     # Data processing service
│   │   └── cache_service.py    # Caching service
│   │
│   ├── core/                   # Core utilities
│   │   ├── __init__.py
│   │   ├── exceptions.py       # Custom exceptions
│   │   ├── middleware.py       # Custom middleware
│   │   └── logging.py          # Logging configuration
│   │
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       ├── validators.py       # Custom validators
│       └── helpers.py          # Helper functions
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest configuration
│   ├── test_agents/
│   │   ├── __init__.py
│   │   └── test_chat_agent.py
│   ├── test_api/
│   │   ├── __init__.py
│   │   └── test_chat.py
│   └── test_services/
│       ├── __init__.py
│       └── test_ai_service.py
│
├── docs/                       # Documentation
│   ├── api_docs.md
│   └── deployment.md
│
├── scripts/                    # Utility scripts
│   ├── start_dev.py
│   └── migrate.py
│
├── .env                        # Environment variables
├── .env.example               # Environment template
├── .gitignore                 # Should include venv/
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── pyproject.toml            # Project metadata and tool config
├── Dockerfile
├── docker-compose.yml
└── README.md
```