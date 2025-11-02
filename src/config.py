import os

APP_NAME = "ModelTimeTable"
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
