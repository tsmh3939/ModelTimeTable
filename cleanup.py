
# -*- coding: utf-8 -*-
"""
開発用ファイル・フォルダのクリーンアップスクリプト
Development Files and Folders Cleanup Script

削除対象:
- docs/converted/ (変換済みCSVフォルダ)
- docs/extracted/ (抽出済みCSVフォルダ)
- modeltimetable.db (データベースファイル)
- migrations/ (マイグレーションフォルダ)
"""

import os
import shutil
import sys


def delete_folder(path: str) -> bool:
    """
    フォルダを削除

    Args:
        path: 削除するフォルダのパス

    Returns:
        削除成功: True, 存在しない/失敗: False
    """
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            print(f"✓ 削除しました: {path}")
            return True
        except Exception as e:
            print(f"✗ 削除に失敗しました: {path} - {e}", file=sys.stderr)
            return False
    else:
        print(f"- スキップ: {path} (存在しません)")
        return False


def delete_file(path: str) -> bool:
    """
    ファイルを削除

    Args:
        path: 削除するファイルのパス

    Returns:
        削除成功: True, 存在しない/失敗: False
    """
    if os.path.exists(path):
        try:
            os.remove(path)
            print(f"✓ 削除しました: {path}")
            return True
        except Exception as e:
            print(f"✗ 削除に失敗しました: {path} - {e}", file=sys.stderr)
            return False
    else:
        print(f"- スキップ: {path} (存在しません)")
        return False


def main():
    """メイン処理"""
    print("=" * 70)
    print("開発用ファイル・フォルダのクリーンアップ")
    print("=" * 70)
    print()
    print("以下のファイル・フォルダを削除します:")
    print("  - docs/converted/    (変換済みCSVフォルダ)")
    print("  - docs/extracted/    (抽出済みCSVフォルダ)")
    print("  - modeltimetable.db  (データベースファイル)")
    print("  - migrations/        (マイグレーションフォルダ)")
    print()

    # 確認
    response = input("削除してもよろしいですか？ (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("\nキャンセルしました。")
        sys.exit(0)

    print("\n" + "=" * 70)
    print("削除処理を開始します...")
    print("=" * 70)
    print()

    # 削除対象のパス
    targets = [
        ("folder", "docs/converted"),
        ("folder", "docs/extracted"),
        ("file", "src/modeltimetable.db"),
        ("folder", "migrations"),
    ]

    # 削除実行
    deleted_count = 0
    for target_type, target_path in targets:
        if target_type == "folder":
            if delete_folder(target_path):
                deleted_count += 1
        else:  # file
            if delete_file(target_path):
                deleted_count += 1

    print()
    print("=" * 70)
    print(f"クリーンアップ完了: {deleted_count}件のファイル・フォルダを削除しました")
    print("=" * 70)


if __name__ == '__main__':
    main()
