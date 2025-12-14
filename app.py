
from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'testdb'),
        user=os.environ.get('DB_USER', 'testuser'),
        password=os.environ.get('DB_PASSWORD', 'testpass')
    )
    return conn

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/items', methods=['GET', 'POST'])
def items():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        data = request.json
        cur.execute("INSERT INTO items (name) VALUES (%s) RETURNING id;", (data['name'],))
        item_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'id': item_id, 'name': data['name']}), 201
    else:
        cur.execute("SELECT id, name FROM items;")
        items = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{'id': i[0], 'name': i[1]} for i in items])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
