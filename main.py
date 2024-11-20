import json

class Book:
    def __init__(self, id, title, author, year, available=True):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.available = available

    def __str__(self):
        return f"{self.id}: {self.title} by {self.author} ({self.year})"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "available": self.available,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            available=data["available"],
        )


class Library:
    def __init__(self, data_file="library.json"):
        self.data_file = data_file
        self.books = self.load_books()

    def load_books(self):
        try:
            with open(self.data_file, "r") as file:
                data = json.load(file)
                return [Book.from_dict(book) for book in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_books(self):
        with open(self.data_file, "w") as file:
            json.dump([book.to_dict() for book in self.books], file, indent=4)

    def add_book(self, book):
        if any(b.id == book.id for b in self.books):
            return f"Книга с ID {book.id} уже существует."
        self.books.append(book)
        self.save_books()
        return f"Книга добавлена в библиотеку: {book}"

    def remove_book(self, book_id):
        book = next((b for b in self.books if b.id == book_id), None)
        if book:
            self.books.remove(book)
            self.save_books()
            return f"Книга удалена из библиотеки: {book}"
        return f"Книга с ID {book_id} не найдена."

    def list_books(self):
        if not self.books:
            return "В библиотеке нет книг."
        return "Список книг в библиотеке:\n" + "\n".join(str(book) for book in self.books)

    def search_book(self, book_id):
        return next((b for b in self.books if b.id == book_id), None)


class User:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book_id, library):
        book = library.search_book(book_id)
        if not book:
            return f"Книга с ID {book_id} не найдена."
        if book.available:
            book.available = False
            self.borrowed_books.append(book)
            library.save_books()
            return f"{self.name} взял книгу: {book.title}"
        return f"Книга {book.title} недоступна для выдачи."

    def return_book(self, book_id, library):
        book = next((b for b in self.borrowed_books if b.id == book_id), None)
        if not book:
            return f"Книга с ID {book_id} не найдена у {self.name}."
        book.available = True
        self.borrowed_books.remove(book)
        library.save_books()
        return f"{self.name} вернул книгу: {book.title}"

    def list_borrowed_books(self):
        if not self.borrowed_books:
            return f"У {self.name} нет взятых книг."
        return f"Список взятых книг {self.name}:\n" + "\n".join(str(book) for book in self.borrowed_books)


# Пример использования
library = Library()
user = User("Иван")

# Добавляем книги
print(library.add_book(Book(1, "1984", "George Orwell", 1949)))
print(library.add_book(Book(2, "To Kill a Mockingbird", "Harper Lee", 1960)))
print(library.add_book(Book(3, "Moby-Dick", "Herman Melville", 1851)))

# Список книг
print(library.list_books())

# Пользователь берет книгу
print(user.borrow_book(1, library))
print(user.borrow_book(1, library))  # Повторное взятие той же книги

# Возврат книги
print(user.return_book(1, library))

# Список книг после возврата
print(library.list_books())
