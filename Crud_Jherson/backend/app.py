from flask import Flask  
from flask_cors import CORS  # Importa CORS, que permite solicitudes desde orígenes cruzados (cross-origin resource sharing)
from flask import jsonify, request  # Importa funciones de Flask para manejar respuestas JSON y obtener datos de solicitudes HTTP
import pymysql  # Importa pymysql para interactuar con una base de datos MySQL

app = Flask(__name__)  # Crea una instancia de la aplicación Flask
CORS(app)  # Habilita CORS para permitir solicitudes desde cualquier dominio (útil si la API es usada por clientes externos)

# Función para conectar con la base de datos MySQL
def conectar(vhost, vuser, vpass, vdb):
    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset='utf8mb4')  # Conexión con la base de datos
    return conn  # Devuelve la conexión

# Ruta raíz de la API ("/"), que realiza una consulta a la base de datos para obtener todos los registros
@app.route("/")
def consulta_general():
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')  # Conecta con la base de datos
        cur = conn.cursor()  # Crea un cursor para ejecutar consultas SQL
        cur.execute("""SELECT * FROM baul""")  # Ejecuta una consulta SQL para obtener todos los registros de la tabla "baul"
        datos = cur.fetchall()  # Obtiene todos los resultados de la consulta
        data = []  # Lista vacía para almacenar los resultados
        for row in datos:  # Itera sobre cada fila de los resultados
            dato = {'id_baul': row[0], 'Plataforma': row[1], 'usuario': row[2], 'clave': row[3]}  # Crea un diccionario para cada registro
            data.append(dato)  # Añade el diccionario a la lista de datos
        cur.close()  # Cierra el cursor
        conn.close()  # Cierra la conexión a la base de datos
        return jsonify({'baul': data, 'mensaje': 'Baul de contraseñas'})  # Devuelve los datos como respuesta JSON
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})  # Si ocurre un error, devuelve un mensaje de error

# Ruta para consulta individual de un registro por código ("<codigo>"), con el método GET
@app.route("/consulta_individual/<codigo>", methods=['GET'])
def consulta_individual(codigo):
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena') 
        cur = conn.cursor()  # Crea el cursor
        cur.execute("""SELECT * FROM baul WHERE id_baul = %s""", (codigo,))  
        datos = cur.fetchone()  
        cur.close()  
        conn.close()  
        if datos is not None:
            dato = {'id_baul': datos[0], 'Plataforma': datos[1], 'usuario': datos[2], 'clave': datos[3]}  # Crea un diccionario con los datos
            return jsonify({'baul': dato, 'mensaje': 'Registro encontrado'})  # Devuelve el registro como respuesta JSON
        else:
            return jsonify({'mensaje': 'Registro no encontrado'})  # Si no se encuentra el registro, devuelve un mensaje indicando eso
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})  # En caso de error, devuelve un mensaje de error

# Ruta para registrar una nueva entrada en la base de datos (método POST)
@app.route("/registro/", methods=['POST'])
def registro():
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')  # Conecta con la base de datos
        cur = conn.cursor()  # Crea el cursor
        # Inserta un nuevo registro en la tabla "baul" con los datos recibidos en la solicitud JSON
        x = cur.execute("""INSERT INTO baul (plataforma, usuario, clave) VALUES ('{0}', '{1}', '{2}')""".format(
            request.json['plataforma'],  # Toma el valor de "plataforma" del JSON
            request.json['usuario'],  # Toma el valor de "usuario" del JSON
            request.json['clave']  # Toma el valor de "clave" del JSON
        ))
        conn.commit()  # Confirma la transacción (inserción de datos)
        cur.close()  # Cierra el cursor
        conn.close()  # Cierra la conexión a la base de datos
        return jsonify({'mensaje': 'Registro agregado'})  # Devuelve un mensaje indicando que el registro fue agregado
    except Exception as ex:
        print(ex)  # Imprime el error en la consola (en caso de fallo)
        return jsonify({'mensaje': 'Error'})  # Devuelve un mensaje de error

# Ruta para eliminar un registro por código (método DELETE)
@app.route("/eliminar/<codigo>", methods=['DELETE'])
def eliminar(codigo):
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')  # Conecta con la base de datos
        cur = conn.cursor()  # Crea el cursor
        cur.execute("""DELETE FROM baul WHERE id_baul = {0}""".format(codigo))  # Elimina el registro con el ID especificado
        conn.commit()  # Confirma la transacción (eliminación de datos)
        cur.close()  # Cierra el cursor
        conn.close()  # Cierra la conexión
        return jsonify({'mensaje': 'Eliminado'})  # Devuelve un mensaje indicando que el registro fue eliminado
    except Exception as ex:
        print(ex)  # Imprime el error en la consola
        return jsonify({'mensaje': 'Error'})  # Devuelve un mensaje de error

# Ruta para actualizar un registro por código (método PUT)
@app.route("/actualizar/<codigo>", methods=['PUT'])
def actualizar(codigo):
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')  # Conecta con la base de datos
        cur = conn.cursor()  # Crea el cursor
        # Actualiza el registro con el ID especificado con los nuevos datos recibidos en la solicitud JSON
        x = cur.execute("""UPDATE baul SET plataforma = '{0}', usuario = '{1}', clave = '{2}' WHERE id_baul = {3}""".format(
            request.json['plataforma'],  # Nuevo valor para "plataforma"
            request.json['usuario'],  # Nuevo valor para "usuario"
            request.json['clave'],  # Nuevo valor para "clave"
            codigo  # ID del registro a actualizar
        ))
        conn.commit()  # Confirma la transacción (actualización de datos)
        cur.close()  # Cierra el cursor
        conn.close()  # Cierra la conexión
        return jsonify({'mensaje': 'Registro actualizado'})  # Devuelve un mensaje indicando que el registro fue actualizado
    except Exception as ex:
        print(ex)  # Imprime el error en la consola
        return jsonify({'mensaje': 'Error'})  # Devuelve un mensaje de error

# Inicia la aplicación Flask cuando el archivo se ejecuta directamente
if __name__ == "__main__":
    app.run(debug=True)  # Inicia el servidor web en modo debug (para desarrollo)



                 

            
            
