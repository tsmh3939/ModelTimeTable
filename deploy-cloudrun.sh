#!/bin/bash
# Google Cloud Runへのデプロイスクリプト

set -e

# 設定
PROJECT_ID="${GCP_PROJECT_ID:-your-project-id}"
SERVICE_NAME="${SERVICE_NAME:-modeltimetable}"
REGION="${GCP_REGION:-asia-northeast1}"
DOCKERFILE="Dockerfile.cloudrun"

echo "=========================================="
echo "Google Cloud Runへのデプロイ"
echo "=========================================="
echo "プロジェクトID: $PROJECT_ID"
echo "サービス名: $SERVICE_NAME"
echo "リージョン: $REGION"
echo ""

# プロジェクトIDが設定されているか確認
if [ "$PROJECT_ID" = "your-project-id" ]; then
    echo "エラー: GCP_PROJECT_ID環境変数を設定してください"
    echo "例: export GCP_PROJECT_ID=your-actual-project-id"
    exit 1
fi

# Google Cloud CLIがインストールされているか確認
if ! command -v gcloud &> /dev/null; then
    echo "エラー: Google Cloud CLI (gcloud) がインストールされていません"
    echo "https://cloud.google.com/sdk/docs/install からインストールしてください"
    exit 1
fi

# プロジェクトを設定
echo "プロジェクトを設定中..."
gcloud config set project $PROJECT_ID

# Cloud Run APIを有効化（初回のみ必要）
echo "必要なAPIを有効化中..."
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# デプロイ
echo ""
echo "Cloud Runにデプロイ中..."
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars="FLASK_DEBUG=false,FLASK_DB_NAME=modeltimetable.db" \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10 \
  --dockerfile $DOCKERFILE

echo ""
echo "=========================================="
echo "✅ デプロイ完了！"
echo "=========================================="
echo ""
echo "サービスURL:"
gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)'