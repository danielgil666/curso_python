import csv

# 1. Primero defines la clase
class Animal:
    def __init__(self, nombre, clase, caracteristicas):
        self.nombre = nombre
        self.clase = clase
        self.caracteristicas = caracteristicas

    def __str__(self):
        return f"{self.nombre} ({self.clase}) - {self.caracteristicas}"

# 2. Luego tus funciones (la que ya tenías y la de cargar)
def cargar_csv(ruta):
    datos = []
    try:
        with open(ruta, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                datos.append(row)
    except FileNotFoundError:
        pass # Si no existe, devuelve lista vacía
    return datos

def guardar_csv(ruta, lista_objetos):
    with open(ruta, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["nombre", "clase", "caracteristicas"])
        writer.writeheader()
        for obj in lista_objetos:
            writer.writerow({
                "nombre": obj.nombre, 
                "clase": obj.clase, 
                "caracteristicas": obj.caracteristicas
            })