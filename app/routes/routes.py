from flask import Blueprint, jsonify, request, current_app
from app.utils.config import Config
main = Blueprint('main', __name__)
 
@main.route('/api/users', methods=['POST'])
def create_user():
    try:
        # Obtén los datos del cuerpo de la solicitud
        data = request.get_json()

        # Validación de datos: Asegúrate de que todos los campos estén presentes
        if not data:
            return jsonify({'message': 'Request body is required'}), 400

        missing_fields = []
        if not data.get('userName'):
            missing_fields.append('userName')
        if not data.get('password'):
            missing_fields.append('password')
        if not data.get('email'):
            missing_fields.append('email')

        if missing_fields:
            return jsonify({'message': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        userName = data['userName']
        password = data['password']
        email = data['email']

        # Configuración y conexión a la base de datos
        config = Config()
        db_connection = config.get_db_connection()
        cursor = db_connection.cursor()

        # Verificar si userName o email ya existen
        check_query = """
        SELECT COUNT(*) FROM user WHERE userName = %s OR email = %s;
        """
        cursor.execute(check_query, (userName, email))
        result = cursor.fetchone()

        if result[0] > 0:
            return jsonify({'message': 'UserName or Email already exists'}), 409

        # Inserción de usuario en la tabla
        insert_query = """
        INSERT INTO user (userName, password, email) 
        VALUES (%s, %s, %s);
        """
        cursor.execute(insert_query, (userName, password, email))

        # Confirmar los cambios
        db_connection.commit()

        return jsonify({'message': 'User created successfully!'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Cierra la conexión
        if 'db_connection' in locals() and db_connection:
            cursor.close()
            db_connection.close()

@main.route('/api', methods=['GET'])
def suggest_images():
    return jsonify({"test": "hola"}) 
    
@main.route('/api/db-test', methods=['GET'])
def db_test():
    try:
        # Crea una instancia de Config
        config = Config()  
        
        # Usa la instancia para obtener la conexión
        db_connection = config.get_db_connection()
        cursor = db_connection.cursor()

        # Ejecuta la consulta
        cursor.execute("SELECT DATABASE();")
        database_name = cursor.fetchone()

        return jsonify({"message": "Database connection successful!", "database": database_name[0]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@main.route('/apis/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Test route working!"})

@main.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validate input
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    
    username = data['username']
    password = data['password']

    return jsonify({"success": ""})