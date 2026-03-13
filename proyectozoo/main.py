from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Input, Label, RichLog
from textual.containers import Vertical, Horizontal
from funciones_auxiliares import Animal, cargar_csv, guardar_csv

class ZooApp(App):
    CSS = """
    Input { margin-bottom: 1; }
    Button { margin-bottom: 1; }
    #pantalla { height: 10; border: solid green; margin-top: 1;}
    """

    def on_mount(self):
        # 1. Cargar datos al iniciar
        self.datos_csv = cargar_csv("zoo.csv")
        # Convierte los diccionarios a objetos Animal
        self.animales = [Animal(d['nombre'], d['clase'], d['caracteristicas']) for d in self.datos_csv]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("=== SISTEMA ZOOLÓGICO ===", id="titulo")
        
        with Horizontal():
            with Vertical():
                yield Input(placeholder="Escribe clase (ej. Mamifero)", id="input_clase")
                yield Button("Listar por Clase", id="btn_clase", variant="primary")
                
                yield Input(placeholder="Escribe característica (ej. plumas)", id="input_carac")
                yield Button("Listar por Característica", id="btn_carac", variant="primary")
            
            with Vertical():
                yield Label("Agregar Nuevo Animal:")
                yield Input(placeholder="Nombre del animal", id="in_nombre")
                yield Input(placeholder="Clase (ej. Ave)", id="in_clase")
                yield Input(placeholder="Características (ej. vuela, pico)", id="in_carac")
                yield Button("Agregar Animal", id="btn_agregar", variant="success")
        
        yield RichLog(id="pantalla")
        yield Button("Guardar y Salir", id="btn_salir", variant="error")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        pantalla = self.query_one("#pantalla", RichLog)
        
        # Filtrar por Clase
        if event.button.id == "btn_clase":
            pantalla.clear()
            busqueda = self.query_one("#input_clase", Input).value.lower()
            encontrados = [a for a in self.animales if busqueda in a.clase.lower()]
            for a in encontrados: 
                pantalla.write(str(a)) # Llama al método __str__ de tu clase
                
        # Filtrar por Característica
        elif event.button.id == "btn_carac":
            pantalla.clear()
            busqueda = self.query_one("#input_carac", Input).value.lower()
            encontrados = [a for a in self.animales if busqueda in a.caracteristicas.lower()]
            for a in encontrados: 
                pantalla.write(str(a))
                
        # Agregar Animal
        elif event.button.id == "btn_agregar":
            nom = self.query_one("#in_nombre", Input).value
            cla = self.query_one("#in_clase", Input).value
            car = self.query_one("#in_carac", Input).value
            
            if nom and cla and car:
                nuevo = Animal(nom, cla, car)
                self.animales.append(nuevo)
                pantalla.write(f"¡Éxito! Agregado: {nuevo}")
            else:
                pantalla.write("Error: Llena los 3 campos para agregar.")
                
        # Guardar cambios y salir
        elif event.button.id == "btn_salir":
            guardar_csv("zoo.csv", self.animales)
            self.exit()

if __name__ == "__main__":
    ZooApp().run()