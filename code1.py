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


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, title):
        self.books = [book for book in self.books if book.title != title]

    def find_book(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return None


# Приклад використання:
author1 = Author("Тарас", "Шевченко")
book1 = Book("Кобзар", author1, 1840)

library = Library()
library.add_book(book1)

print(library.find_book("Кобзар"))
library.remove_book("Кобзар")
print(library.find_book("Кобзар"))  # None
