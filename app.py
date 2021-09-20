from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask.helpers import flash
from datetime import datetime

app = Flask(__name__)

# Conección a MySQL
mysql = MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskempleados'
mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'

# Index ------------------------------------------------------------------------------------------------------------------------


@app.route('/')
def index():
    sql = 'SELECT * FROM empleados'
    cur = mysql.connection.cursor()
    cur.execute(sql)
    # Con esto capturlo los valores consultados de la base de datos para mostrarlos
    data = cur.fetchall()
    mysql.connection.commit()
    return render_template('empleados/index.html', empleados=data)

# Crear ------------------------------------------------------------------------------------------------------------------------


@app.route('/crear')
def create():
    return render_template('empleados/crear.html')

# Store ------------------------------------------------------------------------------------------------------------------------


@app.route('/store', methods=['POST'])
def storage():
    nombre = request.form['nombre']
    correo = request.form['correo']
    foto = request.files['foto']
    now = datetime.now()
    tiempo = now.strftime('%Y%H%M%S')
    if foto.filename != '':
        nuevoNombreFoto = tiempo + '-' + foto.filename
        foto.save('uploads/' + nuevoNombreFoto)
    sql = 'INSERT INTO empleados (nombre, correo, foto) VALUES (%s, %s, %s)'
    datos = (nombre, correo, foto.filename)
    cur = mysql.connection.cursor()
    cur.execute(sql, datos)
    mysql.connection.commit()
    flash('Datos guardados correctamente')
    return redirect(url_for('index'))

# Editar ---------------------------------------------------------------------------------------------------------------------


@app.route('/editar/<id>')
def editar_empleado():
    sql = 'SELECT * FROM empelados WHERE id = %s;'
    cur = mysql.connection.cursor()
    cur.execute(sql, (id))
    data = cur.fetchall()
    print(data[0])
    return 'recibido'


# Actualizar -----------------------------------------------------------------------------------------------------------------


# Eliminar -------------------------------------------------------------------------------------------------------------------


@app.route('/eliminar/<string:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM empleados WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Datos elimiandos correctamente')
    return redirect(url_for('index'))

# Debugger -------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(port=5000, debug=True)
