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
if [ ! -f "src/app.db" ]; then
    echo "Creating database..."
    flask db upgrade
else
    echo "Applying pending migrations..."
    flask db upgrade
fi

echo "Database setup complete!"

# サンプルデータを挿入
echo "Seeding database..."
python seed_data.py

# アプリケーションを起動
echo "Starting application..."
exec python app.py
