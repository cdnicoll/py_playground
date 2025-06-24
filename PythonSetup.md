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