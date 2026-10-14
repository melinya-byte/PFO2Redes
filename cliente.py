import requests

BASE = 'http://127.0.0.1:5000'

def registrar():
    usuario = input('Usuario: ')
    contrasena = input('Contraseña: ')
    r = requests.post(f'{BASE}/registro', json={'usuario': usuario, 'contraseña': contrasena})
    print(r.json())

def login():
    usuario = input('Usuario: ')
    contrasena = input('Contraseña: ')
    r = requests.post(f'{BASE}/login', json={'usuario': usuario, 'contraseña': contrasena})
    print(r.json())

def ver_tareas():
    r = requests.get(f'{BASE}/tareas')
    print(r.text)

while True:
    print('1. Registrarse')
    print('2. Iniciar sesión')
    print('3. Ver tareas')
    print('4. Salir')
    op = input('Opción: ')
    if op == '1': registrar()
    elif op == '2': login()
    elif op == '3': ver_tareas()
    elif op == '4': break