"""
サンプルデータを挿入するスクリプト
実行方法: python seed_data.py
"""
from src import app, db
from src.models import User
from datetime import datetime
import os
import subprocess

def check_and_create_tables():
    """テーブルが存在しない場合は作成"""
    with app.app_context():
        try:
            # テーブルの存在確認
            User.query.first()
            print("✓ データベーステーブルが存在します")
            return True
        except Exception:
            print("⚠ データベーステーブルが存在しません")
            print("データベースを初期化します...")

            # マイグレーションディレクトリが存在するか確認
            if not os.path.exists('migrations'):
                print("  - flask db init を実行中...")
                subprocess.run(['flask', 'db', 'init'], check=True)

            print("  - flask db migrate を実行中...")
            subprocess.run(['flask', 'db', 'migrate', '-m', 'Initial migration'], check=True)

            print("  - flask db upgrade を実行中...")
            subprocess.run(['flask', 'db', 'upgrade'], check=True)

            print("✓ データベースの初期化が完了しました")
            return True

def seed_database():
    """データベースにサンプルデータを挿入"""
    with app.app_context():
        # テーブルの存在確認と作成
        if not check_and_create_tables():
            print("エラー: データベースの初期化に失敗しました")
            return

        # 既存のユーザーを確認
        print("\n既存のデータを確認中...")
        existing_users = User.query.all()
        print(f"既存ユーザー数: {len(existing_users)}")

        # サンプルユーザーデータ
        sample_users = [
            {
                'username': 'admin',
                'email': 'admin@example.com'
            },
            {
                'username': 'taro',
                'email': 'taro@example.com'
            },
            {
                'username': 'hanako',
                'email': 'hanako@example.com'
            },
            {
                'username': 'john_doe',
                'email': 'john@example.com'
            },
            {
                'username': 'jane_smith',
                'email': 'jane@example.com'
            }
        ]

        print("\nサンプルデータを挿入中...")
        added_count = 0
        skipped_count = 0

        for user_data in sample_users:
            # 既存のユーザーかチェック
            existing = User.query.filter_by(username=user_data['username']).first()

            if existing:
                print(f"  ⚠ スキップ: {user_data['username']} (既に存在します)")
                skipped_count += 1
            else:
                new_user = User(
                    username=user_data['username'],
                    email=user_data['email']
                )
                db.session.add(new_user)
                print(f"  ✓ 追加: {user_data['username']} ({user_data['email']})")
                added_count += 1

        # コミット
        try:
            db.session.commit()
            print(f"\n完了! {added_count}件のユーザーを追加しました。({skipped_count}件はスキップ)")

            # 結果を表示
            print("\n現在のユーザー一覧:")
            all_users = User.query.all()
            for user in all_users:
                print(f"  ID: {user.id}, Username: {user.username}, Email: {user.email}, Created: {user.created_at}")

        except Exception as e:
            db.session.rollback()
            print(f"\nエラーが発生しました: {e}")

if __name__ == '__main__':
    print("=" * 60)
    print("サンプルデータ挿入スクリプト")
    print("=" * 60)
    seed_database()