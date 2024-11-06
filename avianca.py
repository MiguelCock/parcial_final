from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import math

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vuelos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ============================ Factorial ============================

@app.route('/factorial/<int:numero>', methods=['GET'])
def calculate_factorial(numero):
    resultado = math.factorial(numero)
    return render_template("factorial.html", numero=numero, resultado=resultado)

# ============================ Vuelos ============================
class Vuelo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # Nacional o Internacional
    precio = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Vuelo {self.nombre}>"


@app.route('/')
def home():
    return "Bienvenido a la gestión de vuelos y cálculo de factorial."


@app.route('/anadir_vuelo', methods=['POST'])
def anadir_vuelo():
    data = request.get_json()
    nombre = data.get('nombre')
    tipo = data.get('tipo')
    precio = data.get('precio')

    if not nombre or tipo not in ['Nacional', 'Internacional'] or not precio:
        return jsonify({"error": "Datos inválidos"}), 400

    nuevo_vuelo = Vuelo(nombre=nombre, tipo=tipo, precio=precio)
    db.session.add(nuevo_vuelo)
    db.session.commit()

    return jsonify({"mensaje": "Vuelo agregado exitosamente", "vuelos": {
        "id": nuevo_vuelo.id,
        "nombre": nuevo_vuelo.nombre,
        "tipo": nuevo_vuelo.tipo,
        "precio": nuevo_vuelo.precio
    }}), 201


@app.route('/vuelos', methods=['GET'])
def vuelos():
    vuelos = Vuelo.query.all()
    informacion_vuelos = [{"id": vuelo.id, "nombre": vuelo.nombre, "tipo": vuelo.tipo, "precio": vuelo.precio} for vuelo in vuelos]
    return jsonify(informacion_vuelos)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
