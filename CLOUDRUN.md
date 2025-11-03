# Google Cloud Runデプロイガイド

このドキュメントでは、ModelTimeTableアプリケーションをGoogle Cloud Runにデプロイする方法を説明します。

## 目次

1. [前提条件](#前提条件)
2. [初回セットアップ](#初回セットアップ)
3. [デプロイ方法](#デプロイ方法)
4. [環境変数の設定](#環境変数の設定)
5. [トラブルシューティング](#トラブルシューティング)

---

## 前提条件

### 必要なもの

1. **Google Cloudアカウント**
   - [Google Cloud Console](https://console.cloud.google.com/)にアクセスできること
   - 請求先アカウントが設定されていること（無料枠あり）

2. **Google Cloud CLI (gcloud)**
   - [インストールガイド](https://cloud.google.com/sdk/docs/install)
   - Windows: `gcloud` コマンドが使えること
   - Mac/Linux: `gcloud` コマンドが使えること

3. **Gitリポジトリ**
   - ソースコードがGitで管理されていること

---

## 初回セットアップ

### 1. Google Cloud CLIをインストール

**Windows:**
```cmd
# インストーラーをダウンロードして実行
https://cloud.google.com/sdk/docs/install
```

**Mac:**
```bash
brew install --cask google-cloud-sdk
```

**Linux:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

### 2. Google Cloud CLIを初期化

```bash
# ログイン
gcloud auth login

# プロジェクトを作成（新規の場合）
gcloud projects create your-project-id --name="ModelTimeTable"

# プロジェクトを設定
gcloud config set project your-project-id
```

### 3. 必要なAPIを有効化

```bash
# Cloud Run API
gcloud services enable run.googleapis.com

# Cloud Build API
gcloud services enable cloudbuild.googleapis.com
```

---

## デプロイ方法

### 方法1: デプロイスクリプトを使用（推奨）

#### Windows

```cmd
# 環境変数を設定
set GCP_PROJECT_ID=your-project-id
set SERVICE_NAME=modeltimetable
set GCP_REGION=asia-northeast1

# デプロイ実行
deploy-cloudrun.bat
```

#### Mac/Linux

```bash
# 環境変数を設定
export GCP_PROJECT_ID=your-project-id
export SERVICE_NAME=modeltimetable
export GCP_REGION=asia-northeast1

# スクリプトに実行権限を付与
chmod +x deploy-cloudrun.sh

# デプロイ実行
./deploy-cloudrun.sh
```

### 方法2: 手動デプロイ

```bash
# プロジェクトを設定
gcloud config set project your-project-id

# Cloud Runにデプロイ
gcloud run deploy modeltimetable \
  --source . \
  --platform managed \
  --region asia-northeast1 \
  --allow-unauthenticated \
  --set-env-vars="FLASK_DEBUG=false,FLASK_DB_NAME=modeltimetable.db" \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10 \
  --dockerfile Dockerfile.cloudrun
```

---

## 環境変数の設定

Cloud Runでは以下の環境変数を設定できます：

| 変数名 | 説明 | デフォルト値 | 推奨値 |
|--------|------|--------------|--------|
| `PORT` | アプリケーションのポート番号 | `8080` | `8080`（Cloud Runが自動設定） |
| `FLASK_DEBUG` | デバッグモード | `false` | `false` |
| `FLASK_DB_NAME` | データベースファイル名 | `modeltimetable.db` | `modeltimetable.db` |

### 環境変数を追加/更新する方法

```bash
gcloud run services update modeltimetable \
  --region asia-northeast1 \
  --set-env-vars="NEW_VAR=value"
```

---

## リソース設定

### メモリとCPU

```bash
# メモリを増やす（256Mi, 512Mi, 1Gi, 2Gi, 4Gi, 8Gi）
gcloud run services update modeltimetable \
  --region asia-northeast1 \
  --memory 1Gi

# CPUを増やす（1, 2, 4, 8）
gcloud run services update modeltimetable \
  --region asia-northeast1 \
  --cpu 2
```

### タイムアウトとインスタンス数

```bash
# タイムアウトを設定（最大3600秒）
gcloud run services update modeltimetable \
  --region asia-northeast1 \
  --timeout 600

# 最大インスタンス数を設定
gcloud run services update modeltimetable \
  --region asia-northeast1 \
  --max-instances 20
```

---

## Cloud Runの特徴

### メリット

1. **完全マネージド**
   - サーバー管理不要
   - 自動スケーリング
   - HTTPS自動設定

2. **従量課金**
   - リクエストがない時は課金されない
   - 無料枠あり（月100万リクエストまで）

3. **高速デプロイ**
   - 数分でデプロイ完了
   - ロールバックも簡単

### 制限事項

1. **ステートレス**
   - SQLiteデータベースは永続化されない
   - コンテナが再起動するとデータが消える
   - **推奨**: Cloud SQL（PostgreSQL/MySQL）を使用

2. **リクエストタイムアウト**
   - デフォルト300秒、最大3600秒

3. **コールドスタート**
   - 長時間アクセスがないとコンテナが停止
   - 再起動に数秒かかる場合がある

---

## データベースの永続化（推奨）

Cloud RunでSQLiteを使用すると、コンテナ再起動時にデータが消えます。本番環境では**Cloud SQL**の使用を推奨します。

### Cloud SQLへの移行手順

1. **Cloud SQLインスタンスを作成**

```bash
gcloud sql instances create modeltimetable-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=asia-northeast1
```

2. **データベースを作成**

```bash
gcloud sql databases create modeltimetable \
  --instance=modeltimetable-db
```

3. **Cloud Runから接続**

```bash
gcloud run services update modeltimetable \
  --region asia-northeast1 \
  --add-cloudsql-instances your-project-id:asia-northeast1:modeltimetable-db \
  --set-env-vars="DATABASE_URL=postgresql://user:password@/modeltimetable?host=/cloudsql/your-project-id:asia-northeast1:modeltimetable-db"
```

---

## ログの確認

```bash
# リアルタイムでログを表示
gcloud run services logs tail modeltimetable --region asia-northeast1

# 最新100件のログを表示
gcloud run services logs read modeltimetable --region asia-northeast1 --limit 100
```

---

## トラブルシューティング

### デプロイが失敗する

```bash
# ビルドログを確認
gcloud builds list --limit=5
gcloud builds log <BUILD_ID>
```

### アプリケーションが起動しない

```bash
# サービスのログを確認
gcloud run services logs tail modeltimetable --region asia-northeast1

# サービスの詳細を確認
gcloud run services describe modeltimetable --region asia-northeast1
```

### メモリ不足エラー

```bash
# メモリを増やす
gcloud run services update modeltimetable \
  --region asia-northeast1 \
  --memory 1Gi
```

### タイムアウトエラー

```bash
# タイムアウトを延長
gcloud run services update modeltimetable \
  --region asia-northeast1 \
  --timeout 600
```

---

## カスタムドメインの設定

1. **ドメインマッピングを作成**

```bash
gcloud run domain-mappings create \
  --service modeltimetable \
  --domain your-domain.com \
  --region asia-northeast1
```

2. **DNSレコードを設定**

表示されたCNAMEレコードをDNSプロバイダーで設定します。

---

## コスト管理

### 無料枠

- リクエスト: 月200万リクエストまで無料
- CPU時間: 月180,000 vCPU秒まで無料
- メモリ: 月360,000 GiB秒まで無料
- ネットワーク: 月1 GBまで無料

### コスト削減のヒント

1. **最小インスタンス数を0に設定**
   ```bash
   gcloud run services update modeltimetable \
     --region asia-northeast1 \
     --min-instances 0
   ```

2. **メモリを適切に設定**
   - 不要に大きなメモリを割り当てない
   - 512Miで十分な場合が多い

3. **リージョンを選択**
   - `asia-northeast1`（東京）は比較的安い
   - アクセス元に近いリージョンを選ぶ

---

## セキュリティ

### 認証を有効化

アプリケーションを一般公開したくない場合：

```bash
# 認証を有効化（IAM認証）
gcloud run services update modeltimetable \
  --region asia-northeast1 \
  --no-allow-unauthenticated
```

### シークレットの管理

機密情報はSecret Managerを使用：

```bash
# シークレットを作成
echo -n "your-secret-key" | gcloud secrets create flask-secret-key --data-file=-

# Cloud Runに設定
gcloud run services update modeltimetable \
  --region asia-northeast1 \
  --update-secrets=SECRET_KEY=flask-secret-key:latest
```

---

## 更新とロールバック

### 新しいバージョンをデプロイ

```bash
# コードを更新後、再度デプロイ
./deploy-cloudrun.sh
```

### 以前のバージョンにロールバック

```bash
# リビジョン一覧を確認
gcloud run revisions list --service modeltimetable --region asia-northeast1

# 特定のリビジョンにトラフィックを切り替え
gcloud run services update-traffic modeltimetable \
  --region asia-northeast1 \
  --to-revisions REVISION_NAME=100
```

---

## 参考リンク

- [Google Cloud Run 公式ドキュメント](https://cloud.google.com/run/docs)
- [Cloud Run 価格](https://cloud.google.com/run/pricing)
- [Cloud Run クイックスタート](https://cloud.google.com/run/docs/quickstarts/build-and-deploy)
- [Cloud SQL 連携](https://cloud.google.com/sql/docs/postgres/connect-run)

---

## サポート

問題が発生した場合は、GitHubのIssuesで報告してください。