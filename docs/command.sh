# Deploy Command
cd C:\Dev\ModelTimeTable
gcloud run deploy modeltimetable --source . --region asia-northeast2 --allow-unauthenticated --set-env-vars="FLASK_APP=app.py,FLASK_DB_NAME=modeltimetable.db,DEBUG=False"

# Git Command
git reset --hard HEAD~1
git pull origin main
