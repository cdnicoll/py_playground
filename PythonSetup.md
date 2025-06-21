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

### 4. Deactivate

```bash
deactivate
```

### 5. Install from `requirements.txt`

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
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
rm get-pip.py
```