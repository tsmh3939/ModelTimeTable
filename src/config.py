import os
import glob
import re


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


def get_latest_csv_file():
    """
    docs/配下の年度CSVファイルから最新のものを取得

    Returns:
        str: 最新のCSVファイルパス (例: 'docs/2026.csv')
    """
    csv_files = glob.glob('docs/[0-9][0-9][0-9][0-9].csv')
    if not csv_files:
        # フォールバック: raw_data.csvを使用
        return 'docs/raw_data.csv'
    # 年度でソートして最新を返す
    return sorted(csv_files)[-1]


def extract_year_from_filename(filename):
    """
    ファイル名から年度を抽出

    Args:
        filename: ファイル名 (例: 'docs/2026.csv' or 'docs/raw_data.csv')

    Returns:
        int or None: 抽出された年度、抽出できない場合はNone
    """
    match = re.search(r'(\d{4})\.csv$', filename)
    if match:
        return int(match.group(1))
    return None


def get_fiscal_year_dict():
    """
    現在のCSVファイルから年度情報を取得して辞書を生成

    Returns:
        dict: 年度情報の辞書
    """
    csv_file = os.environ.get('CSV_FILE', get_latest_csv_file())
    year = extract_year_from_filename(csv_file)

    if year:
        return {
            "ja": f"{year}年度",
            "en": f"Fiscal Year {year}"
        }
    else:
        # デフォルト値（年度が抽出できない場合）
        return {
            "ja": "年度未設定",
            "en": "Fiscal Year Not Set"
        }


# CSVファイルパス（環境変数で上書き可能）
CSV_FILE = os.environ.get('CSV_FILE', get_latest_csv_file())

# 年度情報（CSVファイル名から動的に生成）
FISCAL_YEAR = get_fiscal_year_dict()
