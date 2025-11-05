from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from src import db


# =============================================================================
# マスタテーブル
# =============================================================================

class DayMaster(db.Model):
    """曜日マスタ"""
    __tablename__ = 'day_master'

    day_id: Mapped[int] = mapped_column(primary_key=True)
    day_name: Mapped[str] = mapped_column(String(10))

    # リレーション
    offering_histories: Mapped[List["CourseOfferingHistory"]] = relationship(back_populates='day')

    def __repr__(self):
        return f'<DayMaster {self.day_name}>'


class MajorMaster(db.Model):
    """メジャーマスタ"""
    __tablename__ = 'major_master'

    major_id: Mapped[int] = mapped_column(primary_key=True)
    major_name: Mapped[str] = mapped_column(String(50))

    # リレーション
    timetable_models_major1: Mapped[List["TimetableModel"]] = relationship(foreign_keys='TimetableModel.major1_id', back_populates='major1')
    timetable_models_major2: Mapped[List["TimetableModel"]] = relationship(foreign_keys='TimetableModel.major2_id', back_populates='major2')
    affiliated_majors: Mapped[List["AffiliatedMajor"]] = relationship(back_populates='major')

    def __repr__(self):
        return f'<MajorMaster {self.major_name}>'


class CourseCategoryMaster(db.Model):
    """履修区分マスタ"""
    __tablename__ = 'course_category_master'

    course_category_id: Mapped[int] = mapped_column(primary_key=True)
    course_category_name: Mapped[str] = mapped_column(String(50))

    # リレーション
    courses: Mapped[List["Course"]] = relationship(back_populates='course_category')

    def __repr__(self):
        return f'<CourseCategoryMaster {self.course_category_name}>'


class OfferingCategoryMaster(db.Model):
    """開講区分マスタ"""
    __tablename__ = 'offering_category_master'

    offering_category_id: Mapped[int] = mapped_column(primary_key=True)
    offering_category_name: Mapped[str] = mapped_column(String(50))

    # リレーション
    courses: Mapped[List["Course"]] = relationship(back_populates='offering_category')

    def __repr__(self):
        return f'<OfferingCategoryMaster {self.offering_category_name}>'


class ClassFormatMaster(db.Model):
    """授業形態マスタ"""
    __tablename__ = 'class_format_master'

    class_format_id: Mapped[int] = mapped_column(primary_key=True)
    class_format_name: Mapped[str] = mapped_column(String(50))

    # リレーション
    courses: Mapped[List["Course"]] = relationship(back_populates='class_format')

    def __repr__(self):
        return f'<ClassFormatMaster {self.class_format_name}>'


class CourseTypeMaster(db.Model):
    """授業種別マスタ"""
    __tablename__ = 'course_type_master'

    course_type_id: Mapped[int] = mapped_column(primary_key=True)
    course_type_name: Mapped[str] = mapped_column(String(50))

    # リレーション
    courses: Mapped[List["Course"]] = relationship(back_populates='course_type')

    def __repr__(self):
        return f'<CourseTypeMaster {self.course_type_name}>'


class ClassroomMaster(db.Model):
    """教室マスタ"""
    __tablename__ = 'classroom_master'

    classroom_id: Mapped[int] = mapped_column(primary_key=True)
    classroom_name: Mapped[str] = mapped_column(String(100))

    # リレーション
    course_classrooms: Mapped[List["CourseClassroom"]] = relationship(back_populates='classroom')

    def __repr__(self):
        return f'<ClassroomMaster {self.classroom_name}>'


class InstructorMaster(db.Model):
    """教員マスタ"""
    __tablename__ = 'instructor_master'

    instructor_id: Mapped[int] = mapped_column(primary_key=True)
    instructor_name: Mapped[str] = mapped_column(String(100))

    # リレーション
    course_instructors: Mapped[List["CourseInstructor"]] = relationship(back_populates='instructor')
    main_courses: Mapped[List["Course"]] = relationship(back_populates='main_instructor')

    def __repr__(self):
        return f'<InstructorMaster {self.instructor_name}>'


# =============================================================================
# メインテーブル
# =============================================================================

class TimetableModel(db.Model):
    """時間割モデル"""
    __tablename__ = 'timetable_model'

    timetable_model_id: Mapped[int] = mapped_column(primary_key=True)
    semester: Mapped[int] = mapped_column(Integer)
    major1_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('major_master.major_id'))
    major2_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('major_master.major_id'))

    # リレーション
    major1: Mapped[Optional["MajorMaster"]] = relationship(foreign_keys=[major1_id], back_populates='timetable_models_major1')
    major2: Mapped[Optional["MajorMaster"]] = relationship(foreign_keys=[major2_id], back_populates='timetable_models_major2')
    timetable_subjects: Mapped[List["TimetableSubject"]] = relationship(back_populates='timetable_model')

    def __repr__(self):
        return f'<TimetableModel {self.timetable_model_id} Semester:{self.semester}>'


class Course(db.Model):
    """科目"""
    __tablename__ = 'course'

    timetable_code: Mapped[str] = mapped_column(String(20), primary_key=True)
    syllabus_url: Mapped[Optional[str]] = mapped_column(String(500))
    course_title: Mapped[str] = mapped_column(String(200))
    credits: Mapped[int] = mapped_column(Integer)
    course_category_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('course_category_master.course_category_id'))
    offering_category_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('offering_category_master.offering_category_id'))
    class_format_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('class_format_master.class_format_id'))
    course_type_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('course_type_master.course_type_id'))
    main_instructor_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('instructor_master.instructor_id'))

    # リレーション
    course_category: Mapped[Optional["CourseCategoryMaster"]] = relationship(back_populates='courses')
    offering_category: Mapped[Optional["OfferingCategoryMaster"]] = relationship(back_populates='courses')
    class_format: Mapped[Optional["ClassFormatMaster"]] = relationship(back_populates='courses')
    course_type: Mapped[Optional["CourseTypeMaster"]] = relationship(back_populates='courses')
    main_instructor: Mapped[Optional["InstructorMaster"]] = relationship(back_populates='main_courses')
    timetable_subjects: Mapped[List["TimetableSubject"]] = relationship(back_populates='course')
    offering_histories: Mapped[List["CourseOfferingHistory"]] = relationship(back_populates='course')
    course_classrooms: Mapped[List["CourseClassroom"]] = relationship(back_populates='course')
    course_instructors: Mapped[List["CourseInstructor"]] = relationship(back_populates='course')
    affiliated_majors: Mapped[List["AffiliatedMajor"]] = relationship(back_populates='course')
    grade_years: Mapped[List["GradeYear"]] = relationship(back_populates='course')

    def __repr__(self):
        return f'<Course {self.timetable_code} {self.course_title}>'


class CourseOfferingHistory(db.Model):
    """開講履歴"""
    __tablename__ = 'course_offering_history'

    timetable_code: Mapped[str] = mapped_column(String(20), ForeignKey('course.timetable_code'), primary_key=True)
    day_id: Mapped[int] = mapped_column(Integer, ForeignKey('day_master.day_id'), primary_key=True)
    period: Mapped[int] = mapped_column(Integer)

    # リレーション
    course: Mapped["Course"] = relationship(back_populates='offering_histories')
    day: Mapped["DayMaster"] = relationship(back_populates='offering_histories')

    def __repr__(self):
        return f'<CourseOfferingHistory {self.timetable_code} Day:{self.day_id} Period:{self.period}>'


class GradeYear(db.Model):
    """学年"""
    __tablename__ = 'grade_year'

    timetable_code: Mapped[str] = mapped_column(String(20), ForeignKey('course.timetable_code'), primary_key=True)
    grade_name: Mapped[str] = mapped_column(String(10), primary_key=True)

    # リレーション
    course: Mapped["Course"] = relationship(back_populates='grade_years')

    def __repr__(self):
        return f'<GradeYear {self.timetable_code} Grade:{self.grade_name}>'


# =============================================================================
# 中間テーブル
# =============================================================================

class TimetableSubject(db.Model):
    """時間割科目"""
    __tablename__ = 'timetable_subject'

    timetable_model_id: Mapped[int] = mapped_column(Integer, ForeignKey('timetable_model.timetable_model_id'), primary_key=True)
    timetable_code: Mapped[str] = mapped_column(String(20), ForeignKey('course.timetable_code'), primary_key=True)

    # リレーション
    timetable_model: Mapped["TimetableModel"] = relationship(back_populates='timetable_subjects')
    course: Mapped["Course"] = relationship(back_populates='timetable_subjects')

    def __repr__(self):
        return f'<TimetableSubject Model:{self.timetable_model_id} Code:{self.timetable_code}>'


class CourseClassroom(db.Model):
    """科目教室"""
    __tablename__ = 'course_classroom'

    timetable_code: Mapped[str] = mapped_column(String(20), ForeignKey('course.timetable_code'), primary_key=True)
    classroom_id: Mapped[int] = mapped_column(Integer, ForeignKey('classroom_master.classroom_id'), primary_key=True)

    # リレーション
    course: Mapped["Course"] = relationship(back_populates='course_classrooms')
    classroom: Mapped["ClassroomMaster"] = relationship(back_populates='course_classrooms')

    def __repr__(self):
        return f'<CourseClassroom {self.timetable_code} Classroom:{self.classroom_id}>'


class CourseInstructor(db.Model):
    """科目教員"""
    __tablename__ = 'course_instructor'

    timetable_code: Mapped[str] = mapped_column(String(20), ForeignKey('course.timetable_code'), primary_key=True)
    instructor_id: Mapped[int] = mapped_column(Integer, ForeignKey('instructor_master.instructor_id'), primary_key=True)

    # リレーション
    course: Mapped["Course"] = relationship(back_populates='course_instructors')
    instructor: Mapped["InstructorMaster"] = relationship(back_populates='course_instructors')

    def __repr__(self):
        return f'<CourseInstructor {self.timetable_code} Instructor:{self.instructor_id}>'


class AffiliatedMajor(db.Model):
    """所属メジャー"""
    __tablename__ = 'affiliated_major'

    timetable_code: Mapped[str] = mapped_column(String(20), ForeignKey('course.timetable_code'), primary_key=True)
    major_id: Mapped[int] = mapped_column(Integer, ForeignKey('major_master.major_id'), primary_key=True)
    course_category_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('course_category_master.course_category_id'))

    # リレーション
    course: Mapped["Course"] = relationship(back_populates='affiliated_majors')
    major: Mapped["MajorMaster"] = relationship(back_populates='affiliated_majors')
    course_category: Mapped[Optional["CourseCategoryMaster"]] = relationship()

    def __repr__(self):
        return f'<AffiliatedMajor {self.timetable_code} Major:{self.major_id}>'