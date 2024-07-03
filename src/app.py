#Sistema alumnos Python
from flask import Flask, url_for, render_template, request, redirect, send_from_directory
from flaskext.mysql import MySQL
from datetime import datetime
import os

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'alumnos'

UPLOADS = os.path.join('src/uploads')
app.config['UPLOADS']=UPLOADS

mysql.init_app(app)

@app.route('/fotoalumno/<path:nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(os.path.join('uploads'), nombreFoto)

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

    now = datetime.now()
    print(now)
    tiempo = now.strftime("%Y%H%M%S")
    print(tiempo)

    if _foto.filename != '':
        nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save("src/uploads/" + _foto.filename)

    sql = "INSERT INTO alumnos (nombre, correo, foto) values (%s, %s, %s);"
    datos = (_nombre, _correo, _foto.filename)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = f'SELECT foto FROM alumnos WHERE id="{id}"'
    cursor.execute(sql)

    nombreFoto= cursor.fetchone()[0]

    try:
        os.remove(os.path.join(app.config['UPLOADS'], nombreFoto))
    except:
        pass

    sql = f'DELETE FROM alumnos WHERE id="{id}"'

    cursor.execute(sql)
    conn.commit()

    return redirect('/')

@app.route('/modify/<int:id>')
def modify(id):
    sql = f'SELECT * FROM alumnos WHERE id="{id}"'
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    alumno = cursor.fetchone()
    conn.commit()
    return render_template('alumnos/edit.html',alumno=alumno)

@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    id = request.form['txtId']

    datos = (_nombre, _correo, id)

    conn = mysql.connect()
    cursor = conn.cursor()

    if _foto.filename != '':
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save("src/uploads/" + nuevoNombreFoto)
    
        sql = f'SELECT foto FROM alumnos WHERE id="{id}"'
        cursor.execute(sql)
        conn.commit()

        nombreFoto = cursor.fetchone()[0]

        os.remove(os.path.join(app.config['UPLOADS'], nombreFoto))

        sql = f'UPDATE alumnos SET foto="{nuevoNombreFoto}" WHERE id="{id}";' 
        cursor.execute(sql)
        conn.commit()

    sql = f'UPDATE alumnos SET nombre="{_nombre}", correo="{_correo}" WHERE id="{id}"'
    cursor.execute(sql)
    conn.commit()

    return redirect('/')

if __name__== '__main__':
    app.run(debug=True)
