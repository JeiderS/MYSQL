from flask import Flask, render_template, request, redirect, url_for
import os
import dbase as db

template_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(template_dir, 'templates')

app = Flask(__name__)

@app.route('/')
def inicio():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM usuario")
    myresult = cursor.fetchall()
    
    # Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()  # Cerrar la conexión aquí
    return render_template('index.html', data=insertObject)

@app.route('/usuario', methods=['POST'])
def adicionar():
    username = request.form['username']
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    if username and email and name and password:
        cursor = db.database.cursor()
        sql ="INSERT INTO usuario (username,email,name,password) VALUES (%s,%s,%s,%s)"
        data = (username, email, name, password)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('inicio'))
    
@app.route('/delete/<username>', methods=['GET'])
def delete(username):
    cursor = db.database.cursor()
    # SQL para eliminar el registro basado en el nombre de usuario
    sql = "DELETE FROM users WHERE username = %s"
    data = (username,)
    
    cursor.execute(sql, data)
    db.database.commit()

    return redirect(url_for('inicio'))

@app.route('/edit', methods=['POST'])
def update():
    username = request.form['username']
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    if username and email and name and password:
        cursor = db.database.cursor()
        sql ="  UPDATE users SET username = %s , email = %s, name = %s, password = AES_ENCRYPT(%s,'1067284236') WHERE users.username = %s "
        data = (username, email, name, password, username)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('inicio'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
