# ModelTimeTable

Flaskを使用したWebアプリケーションプロジェクトです。

## プロジェクト構成

```
ModelTimeTable/
├── server.py              # アプリケーションのエントリーポイント
├── requirements.txt       # 依存パッケージ
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

Dockerを使用して、環境構築なしで簡単にアプリケーションを実行できます。

### 前提条件
- Docker と Docker Compose がインストールされていること

### 実行方法

**Docker Composeで実行:**
```bash
# アプリケーションをビルドして起動
docker-compose up --build

# バックグラウンドで実行する場合
docker-compose up -d --build

# 停止
docker-compose down
```

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
