from flask import Flask
app=Flask(__name__)

@app.route("/")
def index():
    return ('<h1>Hello World!</h1>'
            '<a href="/alumnos">Ir a Alumnos</a>')
@app.route("/alumnos")
def get_alumnos():
    return "Retornando todos los alumnos"

if __name__=='__main__':
    app.run(debug=True)