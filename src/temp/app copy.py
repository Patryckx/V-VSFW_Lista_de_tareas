from flask import Flask , render_template ,request ,redirect,url_for
import os
import database as db


template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir,'src','templates')


app = Flask(__name__,template_folder= template_dir)

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