#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Static files collect karo
python manage.py collectstatic --no-input

# Database migrate karo
python manage.py migrate