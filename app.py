from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sqlalchemy import create_engine
import os

app = Flask(__name__)
CORS(app)

# Railway 환경변수 또는 직접 입력
DB_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:비밀번호@호스트:포트/DB이름')
engine = create_engine(DB_URL)

@app.route("/")
def home():
    return "Rental API server is running!"

@app.route("/api/prices")
def get_prices():
    product_id = request.args.get("product_id")
    if not product_id:
        return jsonify({"error": "product_id is required"}), 400
    try:
        df = pd.read_sql(f"SELECT * FROM prices WHERE product_id = {product_id}", engine)
        return df.to_json(orient="records", force_ascii=False)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 예시: 모든 상품 조회
@app.route("/api/products")
def get_products():
    try:
        df = pd.read_sql("SELECT * FROM products", engine)
        return df.to_json(orient="records", force_ascii=False)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)