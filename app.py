from flask import Flask, request, jsonify
from psycopg2 import connect, extras
from cryptography.fernet import Fernet


app = Flask(__name__)
key = Fernet.generate_key()


host = "localhost"
port = 5432
dbname = "usersdb"
user = "postgres"
password = "postgres"



def get_connection():
    conn = connect(host=host, port=port, dbname=dbname, user=user, password=password)
    return conn


# agregar usuario

@app.post("/api/users")
def create_users():
    new_user = request.get_json()
    username = new_user["username"]
    password = Fernet(key).encrypt(bytes(new_user["password"], "utf-8"))

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING *",
        (username, password),
    )
    new_created_user = cur.fetchone()
    print(new_created_user)
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(new_created_user)


# eliminar usuarios

@app.delete("/api/users/<id>")
def delete_users(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute("DELETE FROM users WHERE id = %s RETURNING *", (id))
    user = cur.fetchone()

    print(user)

    conn.commit()

    conn.close()
    cur.close()

    if user is None:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user)

    return "deleting users"


# actualizar usuario

@app.put("/api/users/<id>")
def update_users(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    new_user = request.get_json()
    username = new_user["username"]
    password = Fernet(key).encrypt(bytes(new_user["password"], "utf-8"))

    cur.execute(
        "UPDATE users SET username = %s, password = %s WHERE id = %s RETURNING *",
        (username, password, id))
    
    updated_user = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()
    

    if updated_user is None:
        return jsonify({'massage': 'User not found'}), 404
    


    return jsonify(updated_user)

# obtener usuario

@app.get('/api/users')
def get_users():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)

# obtener unico usuario

@app.get('/api/user/<id>')
def get_user(id):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM users WHERE id = %s', (id))
    user = cur.fetchone()

    if user is None:
        return jsonify({'message': 'User not found'}), 404
    
    

    return jsonify(user)




if __name__ == "__main__":
    app.run(debug=True)
