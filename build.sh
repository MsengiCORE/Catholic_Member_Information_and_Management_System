
#!/usr/bin/env bash

set -Eeuo pipefail

# ==========================================
# CCMIMS - Django Build Script
# Django + PostgreSQL + django-tailwind
# ==========================================

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

VENV_DIR="${VENV_DIR:-venv}"
PYTHON="${PYTHON:-python3}"

echo "=========================================="
echo " Building CCMIMS"
echo "=========================================="

# 1. Verify required files
if [[ ! -f "manage.py" ]]; then
    echo "ERROR: manage.py not found."
    exit 1
fi

if [[ ! -f "requirements.txt" ]]; then
    echo "ERROR: requirements.txt not found."
    exit 1
fi

# 2. Create virtual environment
if [[ ! -d "$VENV_DIR" ]]; then
    echo "Creating virtual environment..."
    "$PYTHON" -m venv "$VENV_DIR"
fi

# 3. Activate virtual environment
source "$VENV_DIR/bin/activate"

# 4. Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# 5. Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# 6. Verify Django configuration
echo "Checking Django configuration..."
python manage.py check

# 7. Build Tailwind CSS
echo "Building Tailwind CSS..."

python manage.py tailwind build

# 8. Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# 9. Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "=========================================="
echo " CCMIMS build completed successfully!"
echo "=========================================="
