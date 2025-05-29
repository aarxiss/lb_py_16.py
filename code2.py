from datetime import date, timedelta

class Author:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return f"'{self.title}' by {self.author} ({self.year})"


class User:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Library:
    def __init__(self):
        self.books = []
        self.borrow_history = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, title):
        self.books = [book for book in self.books if book.title != title]

    def find_book(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return None

    def borrow_book(self, title, user, days=14):
        book = self.find_book(title)
        if book:
            self.books.remove(book)
            due_date = date.today() + timedelta(days=days)
            self.borrow_history.append({'book': book, 'user': user, 'due_date': due_date})
            print(f"Книгу '{title}' видано {user}, термін до {due_date}")
        else:
            print("Книга не знайдена або вже видана")

    def return_book(self, title, user):
        for record in self.borrow_history:
            if record['book'].title == title and record['user'] == user:
                self.books.append(record['book'])
                if date.today() > record['due_date']:
                    print(f"Книга '{title}' повернена із запізненням! Термін був до {record['due_date']}")
                else:
                    print(f"Книга '{title}' успішно повернена")
                self.borrow_history.remove(record)
                return
        print("Запис про видачу не знайдено")


# Тест
author1 = Author("Леся", "Українка")
book1 = Book("Лісова пісня", author1, 1911)
user1 = User("Іван Петренко")

lib = Library()
lib.add_book(book1)

lib.borrow_book("Лісова пісня", user1, days=7)
lib.return_book("Лісова пісня", user1)
