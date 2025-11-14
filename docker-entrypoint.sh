#!/bin/bash
set -e

echo "Waiting for database initialization..."

python cleanup.py

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

python setup.py

exec python app.py
