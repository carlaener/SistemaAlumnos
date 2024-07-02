#Sistema alumnos Python
from flask import Flask
from flask import render_template, request, redirect 
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'alumnos'

mysql.init_app(app)

@app.route('/')
def index():
    sql = "SELECT * FROM alumnos;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    alumnos = cursor.fetchall()
    conn.commit()

    return render_template('alumnos/index.html', alumnos=alumnos)

@app.route('/create')
def create():
    return render_template('alumnos/create.html')

@app.route('/store', methods=["POST"])
def store():
    
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']

    sql = "INSERT INTO alumnos (nombre, correo, foto) values (%s, %s, %s);"
    datos = (_nombre, _correo, _foto.filename)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')

if __name__== '__main__':
    app.run(debug=True)
