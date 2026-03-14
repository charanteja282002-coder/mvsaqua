#!/bin/bash
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate

echo "Seeding initial data..."
python manage.py shell -c "
from store.models import Product
if Product.objects.count() == 0:
    exec(open('seed_data.py').read())
    print('Data seeded!')
else:
    print('Data already exists, skipping seed.')
"
echo "Build complete!"
