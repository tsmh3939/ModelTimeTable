import os


DEFAULT_THEME_NAME = "light"
DEFAULT_LANGUAGE = "ja"


APP_NAME = "ModelTimetable"


SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

# デバッグモード設定（環境変数から取得、デフォルトはFalse）
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')

# 言語設定
SUPPORTED_LANGUAGES = {
    "ja": "日本語",
    "en": "English"
}

FISCAL_YEAR = {
    "ja": "令和7年度",
    "en": "Fiscal Year 2025"
}
