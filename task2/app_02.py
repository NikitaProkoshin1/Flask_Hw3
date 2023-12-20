from flask import Flask, render_template
from model_02 import db, Author, Book
from random import choice

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)

@app.route('/')
def index():
    return 'страница index'

@app.route('/createdb')               # вариант создания БД через страницу HTML для создания БД в проекте
def createdb():
    db.create_all()
    return "db is created"

@app.cli.command("fill-books")
def fill_tables():
    count = 5
    # Добавляем авторов
    for author in range(1, count + 1):
        new_author = Author(name=f'Author{author}', surname=f'Surname{author}')
        db.session.add(new_author)
    db.session.commit()
    # Добавляем книги
    for book in range(1, count ** 2):
        author = choice(range(1, 6))
        new_book = Book(title=f'Title{book}', year=choice(range(1990, 2024)), count=choice(range(1, 999999)),
                        author=author)
        db.session.add(new_book)
    db.session.commit()



@app.route('/all_books/')               # функция-обработчик, которая будет выводить список всех книг с указанием их авторов.
def get_all_books():
    books = Book.query.all()
    context = {'books': books}
    return render_template('books.html', **context)


if __name__ == '__main__':              #запуск приложения
    app.run(debug=True)