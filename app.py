from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sqlalchemy import create_engine
import os

app = Flask(__name__)
CORS(app)

# Railway Postgres DB 연결
DB_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:비번@호스트:포트/railway")
engine = create_engine(DB_URL)

@app.route('/api/products')
def products():
    df = pd.read_sql('SELECT * FROM products', engine)
    return df.to_json(orient="records", force_ascii=False)

@app.route('/api/prices')
def prices():
    pid = request.args.get('product_id')
    df = pd.read_sql(f"SELECT * FROM prices WHERE product_id = {pid}", engine)
    return df.to_json(orient="records", force_ascii=False)

@app.route('/api/rental_companies')
def rental_companies():
    df = pd.read_sql('SELECT * FROM rental_companies', engine)
    return df.to_json(orient="records", force_ascii=False)

if __name__ == "__main__":
    app.run(debug=True)