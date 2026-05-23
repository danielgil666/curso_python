from flask import Flask, render_template, request, redirect, url_for
import database as db
from pdf_functions import scrape_and_process, buscar_palabras
import threading

app = Flask(__name__)

# Inicializar BD al arrancar
with app.app_context():
    db.init_db()

@app.route('/')
def home():
    total_docs, total_words, docs_by_year = db.get_dashboard_stats()
    return render_template('home.html', 
                           total_docs=total_docs, 
                           total_words=total_words, 
                           docs_by_year=docs_by_year)

@app.route('/scrapper', methods=['GET', 'POST'])
def scrapper():
    if request.method == 'POST':
        url_id = request.form.get('url_id')
        url_string = request.form.get('url_string')
        # Hilo en segundo plano para no congelar la app
        thread = threading.Thread(target=scrape_and_process, args=(url_id, url_string))
        thread.start()
        return redirect(url_for('scrapper'))
        
    # Cambio aquí: Usamos la nueva función
    urls_con_docs = db.get_urls_with_documents() 
    return render_template('scrapper.html', urls=urls_con_docs)

@app.route('/configuration', methods=['GET', 'POST'])
def configuration():
    if request.method == 'POST':
        nueva_url = request.form.get('nueva_url')
        if nueva_url:
            db.add_url(nueva_url)
        return redirect(url_for('configuration'))
        
    urls = db.get_all_urls()
    return render_template('configuration.html', urls=urls)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    min_sim = float(request.args.get('min_sim', 0.50)) # 0.50 por defecto
    
    resultados = []
    if query:
        resultados = buscar_palabras(query, min_sim)
        
    return render_template('search.html', query=query, resultados=resultados, min_sim=min_sim)

if __name__ == '__main__':
    app.run(debug=True, port=5000)