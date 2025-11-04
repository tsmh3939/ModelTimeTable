import os

APP_NAME = "ModelTimetable"
DEFAULT_THEME_NAME = "light"
DEBUG = True

# セッション設定
SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

# 言語設定
DEFAULT_LANGUAGE = "ja"
SUPPORTED_LANGUAGES = {
    "ja": "日本語",
    "en": "English"
}

FISCAL_YEAR = {"ja": "令和7年度", "en": "Fiscal Year 2025"}
