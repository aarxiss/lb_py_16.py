import json
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
        self.stats = {
            'popularity': {},  # {title: count}
            'returns': {'total': 0, 'successful': 0},
            'reading_times': {}  # {title: [days, ...]}
        }

    def add_book(self, book):
        self.books.append(book)

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
            self.borrow_history.append({
                'book': book,
                'user': user,
                'borrow_date': date.today(),
                'due_date': due_date
            })
            # 📈 Статистика: популярність
            self.stats['popularity'][title] = self.stats['popularity'].get(title, 0) + 1
            print(f"Книгу '{title}' видано {user}, термін до {due_date}")
        else:
            print("Книга не знайдена або вже видана")

    def return_book(self, title, user):
        for record in self.borrow_history:
            if record['book'].title == title and record['user'] == user:
                self.books.append(record['book'])
                return_date = date.today()
                borrow_date = record['borrow_date']
                reading_days = (return_date - borrow_date).days

                # 📊 Статистика: читання
                self.stats['reading_times'].setdefault(title, []).append(reading_days)

                # 📊 Статистика: повернення
                self.stats['returns']['total'] += 1
                if return_date <= record['due_date']:
                    self.stats['returns']['successful'] += 1

                self.borrow_history.remove(record)

                if return_date > record['due_date']:
                    print(f"Книга '{title}' повернена із запізненням!")
                else:
                    print(f"Книга '{title}' успішно повернена")
                return
        print("Запис про видачу не знайдено")

    def export_stats_to_json(self, filename):
        # Обчислити середній час читання
        avg_reading = {
            title: round(sum(times) / len(times), 2)
            for title, times in self.stats['reading_times'].items()
        }

        return_rate = 0
        if self.stats['returns']['total'] > 0:
            return_rate = round(
                self.stats['returns']['successful'] / self.stats['returns']['total'] * 100, 2
            )

        data = {
            "popularity": self.stats['popularity'],
            "average_reading_days": avg_reading,
            "return_percentage": return_rate
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Статистика збережена у {filename}")
