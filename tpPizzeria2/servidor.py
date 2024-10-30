from flask import Flask, render_template, request, redirect, url_for, Response, session
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
app = Flask(__name__, static_url_path='/static')
load_dotenv()

app.config['MYSQL_DB']  = os.getenv('MYSQL_DB')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL__CURSORCLASS'] = os.getenv('MYSQL__CURSORCLASS')
app.config['MYSQL__KEY'] = os.getenv('MYSQL__KEY')
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

mysql = MySQL(app)

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')

@app.route('/compra')
def compra():
    return render_template('compra.html')

@app.route('/carrito')
def carrito():
    carrito = session.get('carrito', [])
    return render_template('carrito.html', carrito=carrito)

@app.route('/add_product', methods=['POST'])
def add_product():
    product_name = request.form.get('product_name')
    if 'carrito' not in session:
        session['carrito'] = []
    session['carrito'].append(product_name)
    session.modified=True
    
    return redirect(url_for('catalogo'))

@app.route('/remove_product', methods=['POST'])
def remove_product():
    product_name = request.form.get('product_name')
    if 'carrito' in session:
        session['carrito'].remove(product_name)
        session.modified=True
    return redirect(url_for('carrito'))



@app.route('/procesar_pedido', methods=['POST'])
def procesar_pedido():
    nombre = request.form['nombre']
    email = request.form['email']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    metodo_pago = request.form['metodo_pago']
    
    return 'Pedido recibido correctamente'

@app.route("/base")
def base():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM catalogo")
    data = cur.fetchall()
    return render_template( 'carrito.html', pizzas = data)

@app.route("/eliminar/<string:id>")
def eliminar(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM catalogo WHERE id = %s",(id,))
    mysql.connection.commit()
    return redirect(url_for("base"))


if __name__ == '__main__':
    app.run(port=5000, debug=True)

