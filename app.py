import os
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def read_csv(filename):
    path = os.path.join(BASE_DIR, filename)
    try:
        return pd.read_csv(path)
    except Exception as e:
        print(f"❌ CSV read error: {filename}, {e}")
        return None

app = Flask(__name__)
CORS(app)

# Load CSVs
products = read_csv("products.csv")
main_categories = read_csv("main_categories.csv")
sub_categories = read_csv("sub_categories.csv")
brands = read_csv("brands.csv")
prices = read_csv("prices.csv")
rental_companies = read_csv("rental_companies.csv")

@app.route("/api/main_categories")
def get_main_categories():
    try:
        items = main_categories[["id", "name"]].to_dict(orient="records")
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/sub_categories")
def get_sub_categories():
    try:
        items = sub_categories[["id", "name", "main_category_id"]].to_dict(orient="records")
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/brands")
def get_brands():
    try:
        items = brands[["id", "name"]].to_dict(orient="records")
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/products")
def get_products():
    try:
        # Pagination
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 15))
        offset = (page - 1) * limit

        # 필터
        main_category_id = request.args.get("main_category_id", type=int)
        sub_category_id = request.args.get("sub_category_id", type=int)
        brand_id = request.args.get("brand_id", type=int)

        df = products.copy()
        if main_category_id:
            df = df[df["main_category_id"] == main_category_id]
        if sub_category_id:
            df = df[df["sub_category_id"] == sub_category_id]
        if brand_id:
            df = df[df["brand_id"] == brand_id]

        # 만약 컬럼에 결측치(NA) 있으면 fillna로 처리
        df = df.fillna("")

        # 기본 컬럼만 리턴 (필요시 수정)
        cols = [
            "id", "name", "model", "brand_id", "main_category_id", "sub_category_id",
            "image_url", "detail_url", "options"
        ]
        items = df[cols].iloc[offset:offset+limit].to_dict(orient="records")
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/prices")
def get_prices():
    try:
        items = prices.to_dict(orient="records")
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/rental_companies")
def get_rental_companies():
    try:
        items = rental_companies.to_dict(orient="records")
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api")
def root():
    return jsonify({"message": "API is running!"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)