from flask import Flask, jsonify, request
import psycopg2
import redis
import os

app = Flask(__name__)

# Config from environment
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "kubeshop")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "password")
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")

# PostgreSQL connection
conn = psycopg2.connect(
    host=DB_HOST,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = conn.cursor()

# Redis connection
redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/products')
def get_products():
    cursor.execute("SELECT id, name, description, price, image FROM products")
    products = [
        {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "price": float(row[3]),
            "image": row[4]
        }
        for row in cursor.fetchall()
    ]
    return jsonify(products)

@app.route('/cart', methods=['POST'])
def add_to_cart():
    item = request.json
    cart_key = "cart:user1"
    redis_client.hincrby(cart_key, item['id'], 1)
    return jsonify({"message": "Item added to cart"}), 201

@app.route('/checkout', methods=['POST'])
def checkout():
    cart_key = "cart:user1"
    redis_client.delete(cart_key)
    return jsonify({"message": "Checkout successful"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
