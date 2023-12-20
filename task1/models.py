from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()

class GenderEnum(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum(GenderEnum))
    group = db.Column(db.Integer)
    faq = db.Column(db.Integer, db.ForeignKey('faq.id'))

    def __repr__(self):
        return f'Student ({self.name})'


class Faq(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    students = db.relationship('Student', backref='faculty', lazy=True)


# В таблице "Оценки" должны быть следующие поля: id, id студента, название предмета и оценка.
class Estimate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    student = db.relationship('Student', backref='estimates', lazy=True)
    faculty = db.Column(db.String, db.ForeignKey('faq.title'))
    faq = db.relationship('Faq', backref='estimates', lazy=True)
    value = db.Column(db.Integer)

    def __repr__(self):
        return f'{self.value}'