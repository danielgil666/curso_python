import csv

class Book:

    def __init__(self, id, image_name, image_url,title, author,genre_id,genre):
        self.id = id
        self.image_name = image_name
        self.image_url = image_url
        self.title = title
        self.author = author
        self.genre_id = genre_id
        self.genre = genre 

    def __str__(self):
        return f"{self.title:<50} - {self.author:<20} - {self.genre}"
        
    
def load_books(filename:str):
        books = []
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)  # Skip header
            for row in reader:
               books.append(Book(row[0], row[1], row[2], row[3], row[4], int(row[5]), row[6]))
        return books


if __name__ == "__main__":
        book=Book(1, "Dune.jpg", "http://m.media-amazon.com/images/I/81Ua99CURsL._SL1500_.jpg", "TDune", "Frank Herbert", 1, "Science Fiction")
        print(book)

        books=load_books(r"C:\Users\Daniel Gil\Downloads\booklist2000.csv")
        print(len(books))