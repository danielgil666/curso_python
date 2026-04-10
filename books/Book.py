import csv 

class Book:
    def __init__(self, id, image_name, image_url, title, author, genre_id, genre):
        self.id = str(id)
        self.image_name = image_name
        self.image_url = image_url
        self.title = title
        self.author = author
        # Manejo de errores por si genre_id no es un número
        try:
            self.genre_id = int(genre_id)
        except (ValueError, TypeError):
            self.genre_id = 0
        self.genre = genre

    def __str__(self):
        return f"{self.title[:45]:<50} - {self.author[:15]:<20} - {self.genre}"
    
    def __repr__(self):
        return self.__str__()

def load_books(filename: str):
    """Carga los libros desde el CSV"""
    books = []
    try:
        # Usamos utf-8-sig por compatibilidad general
        with open(filename, "r", encoding="utf-8-sig") as file:
            reader = csv.reader(file, delimiter=',')
            
            # NOTA: No usamos next(reader) porque el archivo NO tiene encabezados
            for row in reader:
                if len(row) >= 7:
                    books.append(Book(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        
    return books