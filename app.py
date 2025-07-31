from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# CSV 파일 경로
PRODUCTS_CSV = "products.csv"
PRICES_CSV = "prices.csv"
COMPANIES_CSV = "rental_companies.csv"

# 상품 목록 조회
@app.route("/api/products")
def get_products():
    df = pd.read_csv(PRODUCTS_CSV)
    return jsonify(df.to_dict(orient="records"))

# 특정 상품 가격 조회
@app.route("/api/prices")
def get_prices():
    product_id = request.args.get("product_id")
    df = pd.read_csv(PRICES_CSV)
    if product_id:
        df = df[df["product_id"] == int(product_id)]
    return jsonify(df.to_dict(orient="records"))

# 렌탈 회사 목록 조회
@app.route("/api/rental_companies")
def get_companies():
    df = pd.read_csv(COMPANIES_CSV)
    return jsonify(df.to_dict(orient="records"))

# 기본 메인
@app.route("/")
def index():
    return "렌탈 API 서버 실행중!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)