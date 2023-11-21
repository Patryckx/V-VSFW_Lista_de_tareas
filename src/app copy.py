from flask import Flask , render_template ,request ,redirect,url_for
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import Flask, render_template, request, redirect, url_for, flash, session


import os
import database as db


template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir,'src','templates')


app = Flask(__name__,template_folder= template_dir)
#clave secreta
app.secret_key = 'verificacionsoftware'

#inicio de sesion
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificar si el usuario ya existe en la base de datos
        cursor = db.database.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            # El usuario ya existe
            flash('El usuario ya está registrado. Por favor, inicia sesión.')
            return redirect(url_for('login'))
        else:
            # Insertar el nuevo usuario en la base de datos
            cursor.execute("INSERT INTO usuarios (username, password) VALUES (%s, %s)", (username, password))
            db.database.commit()
            flash('Usuario registrado correctamente. Por favor, inicia sesión.')
            return redirect(url_for('login'))

    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.database.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            # Iniciar sesión exitosa
            session['loggedin'] = True
            session['username'] = username
            flash('Inicio de sesión exitoso.')
            return redirect(url_for('index'))  # Redirigir a index.html después del inicio de sesión exitoso
        else:
            # Credenciales incorrectas, redirigir a la página de inicio de sesión con una señal para mostrar la alerta
            return redirect(url_for('login', login_error='true'))

    return render_template('login.html')

@app.route('/index')
def index():
    # Verificar si el usuario ha iniciado sesión
    if 'loggedin' in session and session['loggedin']:
        # El usuario ha iniciado sesión, se renderiza index.html
        return render_template('index.html')
    else:
        # El usuario no ha iniciado sesión, redirigir al login
        return redirect(url_for('login'))



#Rutas de la aplicacion
@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM tareas")
    myresult = cursor.fetchall()
    #convertir datos a diccionario 
    insertObject =[]
    columName =[colum[0] for colum in cursor.description]
    for record in myresult:
        insertObject.append (dict(zip(columName, record)))
        
    cursor.close()
  
    return render_template('login.html',data=insertObject)

#Ruta para guardar usuarios en la bdd
@app.route('/users',methods=['GET','POST'])
def addtarea():
    Tarea = request.form['Tarea']
    Comentarios = request.form['Comentarios']
    Activos = request.form['Activos']

    if Tarea and Comentarios and Activos:
        cursor = db.database.cursor()
        sql = " INSERT INTO tareas (Tarea, Comentarios, Activos) VALUES (%s, %s, %s)"
        data = (Tarea, Comentarios, Activos)
        cursor.execute(sql,data)
        db.database.commit()
        return redirect(url_for('home'))
    
@app.route('/delete/<string:id>', methods=['POST'])
def delete(id):
        cursor = db.database.cursor()
        sql = "DELETE FROM tareas WHERE id=%s"
        data = (id,)
        cursor.execute(sql,data)
        db.database.commit()
        return redirect(url_for('home'))
    
@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
     Tarea = request.form['Tarea']
     Comentarios = request.form['Comentarios']
     Activos = request.form['Activos']

     if Tarea and Comentarios and Activos:
        cursor = db.database.cursor()
        sql = " UPDATE  tareas  SET Tarea = %s, Comentarios = %s, Activos =%s WHERE id = %s"
        data = (Tarea, Comentarios, Activos, id)
        cursor.execute(sql,data)
        db.database.commit()
        return redirect(url_for('home'))   
     



if __name__ =='__main__':
    app.run(debug=True,port=4000)