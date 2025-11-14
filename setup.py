"""
Main setup script for database initialization and data import
Execute all setup tasks in the correct order
"""

import sys
from setup import seed, extractor, convert, insert
from src.config import CSV_FILE, extract_year_from_filename


def main(csv_file=None):
    """
    Execute all setup tasks in order

    Args:
        csv_file: CSVファイルのパス（Noneの場合はconfig.pyから取得）
    """
    # CSVファイルの決定
    if csv_file is None:
        csv_file = CSV_FILE

    # 年度情報を表示
    year = extract_year_from_filename(csv_file)
    year_display = f"{year}年度" if year else "年度不明"

    print("=" * 60)
    print("Starting setup process...")
    print(f"CSV File: {csv_file}")
    print(f"Academic Year: {year_display}")
    print("=" * 60)

    try:
        # Step 1: Seed master data
        print("\n[1/4] Seeding master data...")
        seed()

        # Step 2: Extract CSV data
        print("\n[2/4] Extracting CSV data...")
        extractor(csv_file)

        # Step 3: Convert CSV data
        print("\n[3/4] Converting CSV data...")
        convert()

        # Step 4: Insert CSV data
        print("\n[4/4] Inserting CSV data...")
        insert()

        print("\n" + "=" * 60)
        print(f"Setup process completed successfully for {year_display}!")
        print("=" * 60)

    except Exception as e:
        print(f"\nSetup process failed: {e}")
        raise


if __name__ == "__main__":
    # コマンドライン引数からCSVファイルを受け取る
    csv_file = sys.argv[1] if len(sys.argv) > 1 else None
    main(csv_file)