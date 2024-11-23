from flask import Blueprint, jsonify, request, current_app
from app.utils.config import Config

main = Blueprint('main', __name__)

@main.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
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

        config = Config()
        db_connection = config.get_db_connection()
        cursor = db_connection.cursor()

        check_query = """
        SELECT COUNT(*) FROM user WHERE userName = %s OR email = %s;
        """
        cursor.execute(check_query, (userName, email))
        result = cursor.fetchone()

        if result[0] > 0:
            return jsonify({'message': 'UserName or Email already exists'}), 409

        insert_query = """
        INSERT INTO user (userName, password, email) 
        VALUES (%s, %s, %s);
        """
        cursor.execute(insert_query, (userName, password, email))
        db_connection.commit()

        return jsonify({'message': 'User created successfully!'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'db_connection' in locals() and db_connection:
            cursor.close()
            db_connection.close()

@main.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Request body is required'}), 400

        update_fields = []
        if 'userName' in data:
            update_fields.append('userName')
        if 'password' in data:
            update_fields.append('password')
        if 'email' in data:
            update_fields.append('email')

        if not update_fields:
            return jsonify({'message': 'No fields to update'}), 400

        userName = data.get('userName')
        password = data.get('password')
        email = data.get('email')

        config = Config()
        db_connection = config.get_db_connection()
        cursor = db_connection.cursor()

        check_query = """
        SELECT COUNT(*) FROM user WHERE id = %s;
        """
        cursor.execute(check_query, (id,))
        result = cursor.fetchone()

        if result[0] == 0:
            return jsonify({'message': 'User not found'}), 404

        if userName:
            check_user_query = """
            SELECT COUNT(*) FROM user WHERE userName = %s AND id != %s;
            """
            cursor.execute(check_user_query, (userName, id))
            if cursor.fetchone()[0] > 0:
                return jsonify({'message': 'UserName already exists'}), 409

        if email:
            check_email_query = """
            SELECT COUNT(*) FROM user WHERE email = %s AND id != %s;
            """
            cursor.execute(check_email_query, (email, id))
            if cursor.fetchone()[0] > 0:
                return jsonify({'message': 'Email already exists'}), 409

        update_query = """
        UPDATE user
        SET userName = %s, password = %s, email = %s
        WHERE id = %s;
        """
        cursor.execute(update_query, (userName, password, email, id))
        db_connection.commit()

        return jsonify({'message': 'User updated successfully!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'db_connection' in locals() and db_connection:
            cursor.close()
            db_connection.close()

@main.route('/api/links', methods=['POST'])
def create_link():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Request body is required'}), 400

        missing_fields = []
        if not data.get('idUser'):
            missing_fields.append('idUser')
        if not data.get('platform'):
            missing_fields.append('platform')
        if not data.get('url'):
            missing_fields.append('url')

        if missing_fields:
            return jsonify({'message': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        idUser = data['idUser']
        platform = data['platform']
        url = data['url']

        config = Config()
        db_connection = config.get_db_connection()
        cursor = db_connection.cursor()

        check_user_query = """
        SELECT COUNT(*) FROM user WHERE idUser = %s;
        """
        cursor.execute(check_user_query, (idUser,))
        if cursor.fetchone()[0] == 0:
            return jsonify({'message': 'User not found'}), 404

        insert_query = """
        INSERT INTO link (idUser, platform, url) 
        VALUES (%s, %s, %s);
        """
        cursor.execute(insert_query, (idUser, platform, url))
        db_connection.commit()

        return jsonify({'message': 'Link created successfully!'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'db_connection' in locals() and db_connection:
            cursor.close()
            db_connection.close()

@main.route('/api/links/<int:idLink>', methods=['PUT'])
def update_link(idLink):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Request body is required'}), 400

        missing_fields = []
        if 'platform' not in data:
            missing_fields.append('platform')
        if 'url' not in data:
            missing_fields.append('url')

        if missing_fields:
            return jsonify({'message': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        platform = data['platform']
        url = data['url']

        config = Config()
        db_connection = config.get_db_connection()
        cursor = db_connection.cursor()

        check_link_query = """
        SELECT COUNT(*) FROM link WHERE idLink = %s;
        """
        cursor.execute(check_link_query, (idLink,))
        if cursor.fetchone()[0] == 0:
            return jsonify({'message': 'Link not found'}), 404

        update_query = """
        UPDATE link 
        SET platform = %s, url = %s 
        WHERE idLink = %s;
        """
        cursor.execute(update_query, (platform, url, idLink))
        db_connection.commit()

        return jsonify({'message': 'Link updated successfully!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'db_connection' in locals() and db_connection:
            cursor.close()
            db_connection.close()

@main.route('/api/links/<int:idLink>', methods=['DELETE'])
def delete_link(idLink):
    try:
        config = Config()
        db_connection = config.get_db_connection()
        cursor = db_connection.cursor()

        check_link_query = """
        SELECT COUNT(*) FROM link WHERE idLink = %s;
        """
        cursor.execute(check_link_query, (idLink,))
        if cursor.fetchone()[0] == 0:
            return jsonify({'message': 'Link not found'}), 404

        delete_query = """
        DELETE FROM link WHERE idLink = %s;
        """
        cursor.execute(delete_query, (idLink,))
        db_connection.commit()

        return jsonify({'message': 'Link deleted successfully!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'db_connection' in locals() and db_connection:
            cursor.close()
            db_connection.close()

@main.route('/api/links', methods=['GET'])
def get_all_links():
    try:
        config = Config()
        db_connection = config.get_db_connection()
        cursor = db_connection.cursor()

        select_query = """
        SELECT idLink, idUser, platform, url FROM link ORDER BY platform ASC;
        """
        cursor.execute(select_query)
        links = cursor.fetchall()

        if not links:
            return jsonify({'message': 'No links found'}), 404

        result = []
        for link in links:
            result.append({
                'idLink': link[0],
                'idUser': link[1],
                'platform': link[2],
                'url': link[3]
            })

        return jsonify({'links': result}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'db_connection' in locals() and db_connection:
            cursor.close()
            db_connection.close()

@main.route('/api', methods=['GET'])
def suggest_images():
    return jsonify({"test": "hola"}) 
    
@main.route('/api/db-test', methods=['GET'])
def db_test():
    try:
        config = Config()
        db_connection = config.get_db_connection()
        cursor = db_connection.cursor()

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
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    
    username = data['username']
    password = data['password']

    return jsonify({"success": ""})
