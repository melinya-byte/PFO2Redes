from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DB = 'tareas.db'

def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contraseña_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json()
    usuario = datos.get('usuario')
    contrasena = datos.get('contraseña')
    if not usuario or not contrasena:
        return jsonify({'error': 'Faltan datos'}), 400
    hash = generate_password_hash(contrasena)
    try:
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (usuario, contraseña_hash) VALUES (?, ?)', (usuario, hash))
        conn.commit()
        conn.close()
        return jsonify({'mensaje': 'Usuario registrado'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'El usuario ya existe'}), 400

@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    usuario = datos.get('usuario')
    contrasena = datos.get('contraseña')
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('SELECT contraseña_hash FROM usuarios WHERE usuario = ?', (usuario,))
    fila = cursor.fetchone()
    conn.close()
    if fila and check_password_hash(fila[0], contrasena):
        return jsonify({'mensaje': 'Login exitoso'}), 200
    else:
        return jsonify({'error': 'Credenciales inválidas'}), 401

@app.route('/tareas', methods=['GET'])
def tareas():
    return '''
    <html>
        <head><title>Bienvenido</title></head>
        <body>
            <h1>¡Bienvenido al sistema de tareas!</h1>
            <p>Has iniciado sesión correctamente.</p>
        </body>
    </html>
    '''

if __name__ == '__main__':
    init_db()
    app.run(debug=True)