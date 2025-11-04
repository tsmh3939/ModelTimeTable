#!/bin/bash
set -e

echo "Waiting for database initialization..."

# マイグレーションディレクトリが存在しない場合は初期化
if [ ! -d "migrations" ]; then
    echo "Initializing database migrations..."
    flask db init
    flask db migrate -m "Initial migration"
fi

flask db upgrade

python seed_master_data.py

exec python app.py
