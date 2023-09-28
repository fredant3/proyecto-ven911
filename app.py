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


@app.get("/api/users")
def get_users():
    return "getting users"


@app.post("/api/users")
def create_users():
    new_user = request.get_json()
    username = new_user["username"]
    password = Fernet(key).encrypt(bytes(new_user['password'], 'utf-8'))

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s) RETURNING *",
                (username, password))
    new_created_user = cur.fetchone()
    print(new_created_user)
    conn.commit()
    cur.close()
    conn.close()
    

    return jsonify(new_created_user)


@app.delete("/api/users")
def delete_users():
    return "deleting users"


@app.put("/api/users")
def update_users():
    return "updating users"


@app.get("/api/users")
def get_uses():
    return "getting user"


if __name__ == "__main__":
    app.run(debug=True)
