# Python 3.13のイメージを使用
FROM python:3.13-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係ファイルをコピー
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションファイルをコピー
COPY . .

# エントリーポイントスクリプトの改行コードを変換して実行権限を付与
RUN sed -i 's/\r$//' docker-entrypoint.sh && chmod +x docker-entrypoint.sh

# ポート5000を公開
EXPOSE 5000

# エントリーポイントスクリプトを実行
CMD ["/bin/bash", "./docker-entrypoint.sh"]
