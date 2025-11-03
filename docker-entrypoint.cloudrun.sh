#!/bin/bash
set -e

echo "Starting Cloud Run deployment..."

# データベースファイル名を設定（Cloud Runでは環境変数から取得）
FLASK_DB_NAME="${FLASK_DB_NAME:-modeltimetable.db}"

# マイグレーションディレクトリが存在しない場合は初期化
if [ ! -d "migrations" ]; then
    echo "Initializing database migrations..."
    flask db init
    flask db migrate -m "Initial migration"
fi

# データベースファイルが存在しない場合、またはマイグレーションが適用されていない場合
if [ ! -f "src/$FLASK_DB_NAME" ]; then
    echo "Creating database..."
    flask db upgrade
else
    echo "Applying pending migrations..."
    flask db upgrade
fi

echo "Database setup complete!"

# データを挿入
echo "Seeding database..."
python src/seed_master_data.py

# Cloud Run環境: Gunicornで起動
echo "Starting application with Gunicorn..."
PORT="${PORT:-8080}"
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 --access-logfile - --error-logfile - "src:app"