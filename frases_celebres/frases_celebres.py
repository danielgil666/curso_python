import csv
import json


class Frase:
    def _init_(self, frase,pelicula):
        self.frase = frase
        self.pelicula = pelicula
    def _str_(self):
        """Devuelve la frase en formato string"""
        return f'"{self.frase}" - {self.pelicula}'
    
    def to_dict(self):
        """Devuelve la frase en formato diccionario"""
        return {
            "frase": self.frase,
            "pelicula": self.pelicula
        }
    def to_json(self):        
        """Devuelve la frase en formato JSON"""
        return json.dumps(self.to_dict())


def carga_archivo_csv(nombre_archivo):
        """Carga las frases desde un archivo CSV y devuelve una lista de objetos Frase"""
        frases = []
        try:
            with open(nombre_archivo, "r", encoding="utf-8-sig") as archivo:
                reader = csv.reader(archivo)
                for row in reader:
                    if len(row) >= 2:
                        frase = Frase(row[0], row[1])
                        frases.append(frase)
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
        return frases   
    
if __name__ == "__main__":
            frases = carga_archivo_csv("frases_consolidadas.csv")
            for frase in frases[0:5]:
                print(frase)