# ModelTimeTable

Flaskを使用したWebアプリケーションプロジェクトです。

## はじめにやること
- [GitHub](https://github.com/tsmh3939/ModelTimeTable)からファイルをダウンロードする
- PythonとDockerのインストール

## エラー発生時
- migration と src/modeltimetable.db を削除してもう一度実行する

## セットアップ方法

### オプション1: 仮想環境で実行（開発環境推奨）

#### 前提条件
- Python 3.13以上がインストールされていること

#### セットアップと終了の手順
- ModelTimeTableのフォルダに移動してから、「python app.pyまでを貼り付けて実行」

```bash
python -m venv venv
venv\Scripts\activate
pip install --no-cache-dir -r requirements.txt
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python app.py

deactivate
```

### オプション2: Dockerで実行

Dockerを使用して、環境構築なしで簡単にアプリケーションを実行できます。

#### 前提条件
- Docker と Docker Compose がインストールされていること
- Docker Desktopが起動していること（Windowsの場合）

#### 実行方法

**Docker Composeで実行（推奨）:**

```bash
docker-compose up --build

docker-compose down
```

### 環境変数

**Docker使用時の注意**: Docker環境で実行する場合、`FLASK_HOST=0.0.0.0` に設定する必要があります（デフォルトで設定済み）。これにより、コンテナ外からアクセスできるようになります。

### カスタムテーマの作成

[src/static/css/custom.css](src/static/css/custom.css) でテーマをカスタマイズできます：
```css
:root:has(input.theme-controller[value=light]:checked),
[data-theme="light"] {
    --color-primary: oklch(50% 0.15 150);
    --color-primary-content: oklch(100% 0 0);
}
```

## 使用しているツール・ライブラリ

### フロントエンド
- **Tailwind CSS** - ユーティリティファーストのCSSフレームワーク
  - 公式サイト: https://tailwindcss.com/

- **daisyUI** - Tailwind CSSのコンポーネントライブラリ
  - 公式サイト: https://daisyui.com/

### その他のリソース
- **OKLCH カラーピッカー** - daisyUIで使用するカラー形式
  - https://oklch.com/

- **Material Design Icons** - アイコンライブラリ
  - https://fonts.google.com/icons
