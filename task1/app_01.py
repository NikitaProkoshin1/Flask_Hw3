from flask import Flask, render_template
from models import db, Student, Faq, GenderEnum, Estimate
from random import choice



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)


@app.route('/')
@app.route('/index/')
def index():
    return 'страница Index'


@app.cli.command("init-db")             #инициализация БД
def init_db():
    db.create_all()
    print('OK')


@app.cli.command("fill-students")       # команда на заполнение табл студенты
def fill_tables():
    count = 5
    # Добавляем факультеты
    for faq in range(1, count + 1):
        new_faq = Faq(title=f'faq{faq}')
        db.session.add(new_faq)
    db.session.commit()
    # Добавляем студентов
    for student in range(1, count ** 2):
        faq = choice(range(1, 6))
        new_student = Student(name=f'Student{student}', surname=f'surname{student}', age=choice(range(18, 100)),
                              gender=choice([GenderEnum.MALE, GenderEnum.FEMALE]), group=choice(range(10, 15)),
                              faq=faq)
        db.session.add(new_student)
    db.session.commit()
    print('Таблица Студенты заполнена')


@app.route('/all_students/')
def get_all():
    students = Student.query.all()
    context = {'students': students}
    return render_template('all_stud.html', **context)



@app.cli.command("fill-estimates")
def fill_tables():
    count = 5
    for _ in range(1, count ** 4):
        student_id = choice([stud.id for stud in Student.query.all()])
        faculty = choice([faq.title for faq in Faq.query.all()])
        value = choice(range(1, 101))
        new_estimate = Estimate(student_id=student_id, faculty=faculty, value=value)
        db.session.add(new_estimate)
    db.session.commit()
    print('Таблица Оценки заполнена')

@app.route('/estimates/')
def get_all_est():
    students = Student.query.all()
    return render_template('all_estimates.html', students=students)



if __name__ == '__main__':
    app.run(debug=True)