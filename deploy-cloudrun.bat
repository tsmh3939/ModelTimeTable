@echo off
REM Google Cloud Runへのデプロイスクリプト (Windows用)

setlocal

REM 設定
if "%GCP_PROJECT_ID%"=="" set GCP_PROJECT_ID=your-project-id
if "%SERVICE_NAME%"=="" set SERVICE_NAME=modeltimetable
if "%GCP_REGION%"=="" set GCP_REGION=asia-northeast1
set DOCKERFILE=Dockerfile.cloudrun

echo ==========================================
echo Google Cloud Runへのデプロイ
echo ==========================================
echo プロジェクトID: %GCP_PROJECT_ID%
echo サービス名: %SERVICE_NAME%
echo リージョン: %GCP_REGION%
echo.

REM プロジェクトIDが設定されているか確認
if "%GCP_PROJECT_ID%"=="your-project-id" (
    echo エラー: GCP_PROJECT_ID環境変数を設定してください
    echo 例: set GCP_PROJECT_ID=your-actual-project-id
    exit /b 1
)

REM Google Cloud CLIがインストールされているか確認
where gcloud >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo エラー: Google Cloud CLI (gcloud^) がインストールされていません
    echo https://cloud.google.com/sdk/docs/install からインストールしてください
    exit /b 1
)

REM プロジェクトを設定
echo プロジェクトを設定中...
gcloud config set project %GCP_PROJECT_ID%

REM Cloud Run APIを有効化（初回のみ必要）
echo 必要なAPIを有効化中...
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

REM デプロイ
echo.
echo Cloud Runにデプロイ中...
gcloud run deploy %SERVICE_NAME% ^
  --source . ^
  --platform managed ^
  --region %GCP_REGION% ^
  --allow-unauthenticated ^
  --set-env-vars="FLASK_DEBUG=false,FLASK_DB_NAME=modeltimetable.db" ^
  --memory 512Mi ^
  --cpu 1 ^
  --timeout 300 ^
  --max-instances 10 ^
  --dockerfile %DOCKERFILE%

echo.
echo ==========================================
echo ✅ デプロイ完了！
echo ==========================================
echo.
echo サービスURL:
gcloud run services describe %SERVICE_NAME% --region %GCP_REGION% --format "value(status.url)"

endlocal