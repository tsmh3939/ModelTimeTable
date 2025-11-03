#!/bin/bash
set -e

echo "Waiting for database initialization..."

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
python seed_master_data.py

# 環境に応じてアプリケーションを起動
if [ "$DEPLOYMENT_ENV" = "production" ]; then
    # 本番環境: Gunicornで起動（Cloud Run用）
    echo "Starting application with Gunicorn (production mode)..."
    PORT="${PORT:-8080}"
    exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 --access-logfile - --error-logfile - "src:app"
else
    # 開発環境: Flask開発サーバーで起動
    echo "Starting application with Flask (development mode)..."
    exec python app.py
fi
