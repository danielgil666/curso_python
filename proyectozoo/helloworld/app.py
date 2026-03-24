from flask import Flask

app = Flask(__name__)

@app.route('/')
def index ():
    return '<html><head><title>HELLO WORLD</title></head><body><h1>Hello World</h1><p>Ir a <a href="/about">About</a></p></body></html>'

@app.route('/about')
def about ():
    return '<html><head><title>About this page</title><body>Everything about this website. Back to <a href="/">Hello World</a></body></html>'
if __name__ == '__main__':
    app.run(debug=True)