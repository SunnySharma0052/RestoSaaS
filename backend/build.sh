#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Static files collect karo
python manage.py collectstatic --no-input

# Database migrate karo
python manage.py migrate

# --- SUPERUSER CREATE KARNE KA JAADU ---
echo "Creating Superuser..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'AdminPass123') if not User.objects.filter(username='admin').exists() else print('Superuser already exists')"