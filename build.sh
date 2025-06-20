#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --prefer-binary -r requirements.txt

python manage.py collectstatic --no-input
