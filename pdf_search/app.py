from flask import Flask, render_template, request

app = Flask(__name__)

# Ruta para la pantalla de Inicio (Home)
@app.route('/')
def home():
    return render_template('home.html')

# Ruta para la pantalla del Scrapper
@app.route('/scrapper')
def scrapper():
    return render_template('scrapper.html')

# Ruta para la pantalla de Configuración
@app.route('/configuration')
def configuration():
    return render_template('configuration.html')

# Ruta para la pantalla de Resultados de Búsqueda
@app.route('/search')
def search():
    # Captura lo que el usuario ponga en la barra de navegación
    query = request.args.get('q', '')
    return render_template('search.html', query=query)

if __name__ == '__main__':
    # debug=True permite ver cambios en tiempo real sin reiniciar el servidor
    app.run(debug=True, port=5000)