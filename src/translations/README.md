# シラバス・時間割システム用語翻訳辞書

シラバス・時間割システムで使用される日本語用語とその英語訳をまとめた辞書ファイルです。

## ファイル構成

### シラバス用語
- **syllabus_terms.json** - JSON形式の用語辞書（多言語対応アプリ向け）
- **syllabus_terms.py** - Python辞書形式（Flaskアプリで直接使用可能）

### データベース用語
- **database_terms.json** - JSON形式のDB用語辞書（テーブル名・フィールド名）
- **database_terms.py** - Python辞書形式（SQLAlchemyモデル定義に使用可能）

### フィールド値定義
- **field_values.json** - JSON形式のフィールド値定義（マスタデータ値）
- **field_values.py** - Python辞書/Enum形式（SQLAlchemyモデルや選択肢に使用可能）

### ドキュメント
- **README.md** - このファイル

## 用語カテゴリ

### 1. 基本情報 (Basic Info)
授業科目名、担当教員、開講学期、曜日時限、単位数など

### 2. ディプロマポリシー (Diploma Policy)
要件年度、要件所属、DP値など

### 3. 授業詳細 (Course Details)
授業概要、到達目標、成績評価、教科書、参考書など

### 4. 授業計画 (Schedule)
授業回数、主題、学習方法と内容など

### 5. 一般用語 (Common Terms)
学期、科目区分、授業形態、曜日、時限など

### 6. アクション (Actions)
ボタンやリンクのラベル（保存、削除、検索など）

## 使用方法

### Python辞書として使用

```python
from src.translations.syllabus_terms import translate, ALL_TERMS, BASIC_INFO

# 単一の用語を翻訳
english = translate("授業科目名")  # "Course Name"

# カテゴリ別に取得
basic_terms = BASIC_INFO
print(basic_terms["単位数"])  # "Credits"

# すべての用語を取得
all_translations = ALL_TERMS
```

### Flaskテンプレートで使用

```python
# views.py
from src.translations.syllabus_terms import ALL_TERMS

@app.route('/syllabus')
def syllabus():
    return render_template('syllabus.html', terms=ALL_TERMS)
```

```html
<!-- syllabus.html -->
<h1>{{ terms['授業科目名'] }}</h1>  <!-- Course Name -->
<label>{{ terms['単位数'] }}</label>  <!-- Credits -->
```

### JSONファイルとして使用

```python
import json

with open('src/translations/syllabus_terms.json', 'r', encoding='utf-8') as f:
    terms = json.load(f)

print(terms['basic_info']['授業科目名'])  # "Course Name"
```

### 多言語対応の例

```python
# config.py
SUPPORTED_LANGUAGES = ['ja', 'en']
DEFAULT_LANGUAGE = 'ja'

# translations/i18n.py
from src.translations.syllabus_terms import ALL_TERMS

def get_text(key, lang='ja'):
    if lang == 'en':
        return ALL_TERMS.get(key, key)
    return key

# 使用例
label = get_text("授業科目名", lang='en')  # "Course Name"
```

## データベース用語の使用方法

### SQLAlchemyモデル定義に使用

```python
from src.translations.database_terms import translate_table, translate_field

# テーブル名を翻訳
table_name = translate_table("科目")  # "Course"

# フィールド名を翻訳
field_name = translate_field("開講科目名")  # "course_title"

# モデル定義例
class Course(db.Model):
    __tablename__ = 'courses'

    timetable_code = db.Column(db.String(20), primary_key=True)
    course_title = db.Column(db.String(200), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
```

### ER図からモデル生成

```python
from src.translations.database_terms import TABLES, FIELDS, TABLE_DESCRIPTIONS

# テーブル情報を取得
for jp_name, en_name in TABLES.items():
    description = TABLE_DESCRIPTIONS.get(en_name, '')
    print(f"class {en_name}(db.Model):")
    print(f"    # {jp_name} - {description}")
```

### データベース移行スクリプトで使用

```python
from src.translations.database_terms import translate_field

# 日本語カラム名を英語に変換
columns = ["時間割コード", "開講科目名", "単位数"]
english_columns = [translate_field(col) for col in columns]
# ['timetable_code', 'course_title', 'credits']
```

## フィールド値定義の使用方法

### マスタテーブルのシーディング

```python
from src.translations.field_values import (
    COURSE_CATEGORY_MASTER,
    DAY_MASTER,
    MAJOR_MASTER
)

# 履修区分マスタのシーディング
for cat_id, names in COURSE_CATEGORY_MASTER.items():
    category = CourseCategory(id=cat_id, name_ja=names['ja'], name_en=names['en'])
    db.session.add(category)

# 曜日マスタのシーディング
for day_id, names in DAY_MASTER.items():
    day = Day(id=day_id, name_ja=names['ja'], name_en=names['en'])
    db.session.add(day)

db.session.commit()
```

### Enumを使用したバリデーション

```python
from src.translations.field_values import CourseCategoryEnum, DayEnum

# モデル定義でEnumを使用
class Course(db.Model):
    category_id = db.Column(db.Integer, nullable=False)

    @validates('category_id')
    def validate_category(self, key, value):
        if value not in [e.value for e in CourseCategoryEnum]:
            raise ValueError(f"Invalid category_id: {value}")
        return value

# 使用例
course = Course(category_id=CourseCategoryEnum.REQUIRED)
```

### フィールド値の翻訳

```python
from src.translations.field_values import (
    get_day_name,
    get_course_category_name,
    get_offering_category_name
)

# 曜日名を取得
day_ja = get_day_name(1, lang='ja')      # "月"
day_en = get_day_name(1, lang='en')      # "Monday"
day_short = get_day_name(1, lang='en', short=True)  # "Mon"

# 履修区分名を取得
category_ja = get_course_category_name(1, lang='ja')  # "必修"
category_en = get_course_category_name(1, lang='en')  # "Required"

# テンプレートで使用
@app.route('/timetable')
def timetable():
    courses = Course.query.all()
    return render_template('timetable.html',
                         courses=courses,
                         get_day_name=get_day_name,
                         get_category_name=get_course_category_name)
```

### Flaskフォームでの選択肢

```python
from src.translations.field_values import COURSE_CATEGORY_MASTER, DAY_MASTER
from flask_wtf import FlaskForm
from wtforms import SelectField

class CourseForm(FlaskForm):
    category = SelectField('履修区分',
                          choices=[(k, v['ja']) for k, v in COURSE_CATEGORY_MASTER.items()])
    day = SelectField('曜日',
                     choices=[(k, v['ja']) for k, v in DAY_MASTER.items()])
```

### 定数としての使用

```python
from src.translations.field_values import PERIODS, SEMESTERS, CREDITS, GRADES

# 時限の範囲チェック
if period in PERIODS:
    print(f"有効な時限: {period}")

# セメスタの選択肢
semester_choices = [(s, f"{s}セメスタ") for s in SEMESTERS]

# 単位数のバリデーション
if credits not in CREDITS:
    raise ValueError(f"無効な単位数: {credits}")
```

## 翻訳の追加・修正

### シラバス用語の追加

```python
# syllabus_terms.py
BASIC_INFO = {
    "新しい用語": "New Term",
}
```

### データベース用語の追加

```python
# database_terms.py
TABLES = {
    "新しいテーブル": "NewTable",
}

FIELDS = {
    "新しいフィールド": "new_field",
}
```

## 参考元

- **シラバス用語**: 和歌山大学シラバスシステム (https://web.wakayama-u.ac.jp/syllabus/)
- **データベース用語**: プロジェクトER図 (`docs/image.png`)
- **フィールド値定義**: プロジェクト仕様書およびER図の注釈
- 大学設置基準に基づく標準的なシラバス項目

## ライセンス

このプロジェクトのライセンスに従います。