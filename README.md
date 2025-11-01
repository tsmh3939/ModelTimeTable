# ModelTimeTable

Flaskを使用したWebアプリケーションプロジェクトです。

## プロジェクト構成

```
ModelTimeTable/
├── server.py             # アプリケーションのエントリーポイント
├── requirements.txt      # 依存パッケージ
├── .gitignore            # Git除外ファイル
├── Dockerfile            # Dockerイメージ定義
├── docker-compose.yml    # Docker Compose設定
├── .dockerignore         # Docker除外ファイル
└── src/
    ├── __init__.py       # Flaskアプリケーションの初期化
    ├── config.py         # 設定ファイル
    ├── views.py          # ルーティングとビュー関数
    ├── templates/        # HTMLテンプレート
    │   ├── base.html
    │   └── index.html
    └── static/           # 静的ファイル
        ├── css/
        │   └── style.css
        ├── js/
        └── images/
```

## セットアップ方法

### オプション1: 仮想環境で実行（開発環境推奨）

#### 前提条件
- Python 3.8以上がインストールされていること

#### セットアップと終了の手順

```bash
python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

flask db init

flask db migrate -m "Initial migration"

flask db upgrade

python server.py

deactivate
```

### オプション2: Dockerで実行

Dockerを使用して、環境構築なしで簡単にアプリケーションを実行できます。

#### 前提条件
- Docker と Docker Compose がインストールされていること

#### 実行方法

**Dockerコマンドで実行:**
```bash
# イメージをビルド
docker build -t modeltimetable .

# コンテナを実行
docker run -p 5000:5000 modeltimetable
```

アプリケーションは `http://localhost:5000` でアクセスできます。

## 利用可能なルート

- `/` - ホームページ
- `/test` - テストページ

## 開発

### 新しいルートの追加

[src/views.py](src/views.py) に新しいルート関数を追加してください。

### テンプレートの編集

HTMLテンプレートは [src/templates/](src/templates/) ディレクトリにあります。

### スタイルの変更

CSSファイルは [src/static/css/](src/static/css/) ディレクトリにあります。

## 設定

アプリケーションの設定は [src/config.py](src/config.py) で管理されています。

### 環境変数

以下の環境変数で実行時の設定をカスタマイズできます：

- `FLASK_HOST`: バインドするホスト（デフォルト: `0.0.0.0`）
- `FLASK_PORT`: 使用するポート（デフォルト: `5000`）
- `FLASK_DEBUG`: デバッグモード（`true` または `false`、デフォルト: `false`）

**Docker使用時の注意**: Docker環境で実行する場合、`FLASK_HOST=0.0.0.0` に設定する必要があります（デフォルトで設定済み）。これにより、コンテナ外からアクセスできるようになります。

**Dockerでのデータベース**: Docker環境では、コンテナ起動時に自動的にデータベースが初期化されます。`migrations/` ディレクトリと `src/app.db` ファイルはホストマシンに永続化されるため、コンテナを再起動してもデータは保持されます。

## データベース

このプロジェクトはFlask-SQLAlchemyとFlask-Migrateを使用してデータベースを管理しています。

### データベース操作

**新しいモデルの追加後:**
```bash
# マイグレーションファイルを生成
flask db migrate -m "説明メッセージ"

# マイグレーションを適用
flask db upgrade
```

**マイグレーションの取り消し:**
```bash
flask db downgrade
```

**現在のマイグレーション履歴を確認:**
```bash
flask db history
```

### モデルの定義

データベースモデルは [src/models.py](src/models.py) で定義されています。

例:
```python
from datetime import datetime
from src import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'
```

## テーマ設定

アプリケーションはdaisyUIを使用した30種類のテーマをサポートしています。

### デフォルトテーマの変更

[src/config.py](src/config.py) の `DEFAULT_THEME_NAME` を変更してください：
```python
DEFAULT_THEME_NAME = "dark"  # light, dark, dim, cupcake, など
```

### カスタムテーマの作成

[src/static/css/custom.css](src/static/css/custom.css) でテーマをカスタマイズできます：
```css
:root:has(input.theme-controller[value=light]:checked),
[data-theme="light"] {
    --color-primary: oklch(50% 0.15 150);
    --color-primary-content: oklch(100% 0 0);
}
```
