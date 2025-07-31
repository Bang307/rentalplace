from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# --- 파일 경로 (같은 폴더면 그냥 파일명) ---
PRODUCTS_CSV = "products.csv"
MAIN_CATEGORIES_CSV = "main_categories.csv"
SUB_CATEGORIES_CSV = "sub_categories.csv"
BRANDS_CSV = "brands.csv"
RENTAL_COMPANIES_CSV = "rental_companies.csv"

# --- 데이터 미리 읽어두기 ---
products_df = pd.read_csv(PRODUCTS_CSV, encoding="utf-8-sig")
main_categories_df = pd.read_csv(MAIN_CATEGORIES_CSV, encoding="utf-8-sig")
sub_categories_df = pd.read_csv(SUB_CATEGORIES_CSV, encoding="utf-8-sig")
brands_df = pd.read_csv(BRANDS_CSV, encoding="utf-8-sig")
rental_companies_df = pd.read_csv(RENTAL_COMPANIES_CSV, encoding="utf-8-sig")

# --- 메인카테고리 API ---
@app.route("/api/main_categories", methods=["GET"])
def get_main_categories():
    return jsonify(main_categories_df.to_dict(orient="records"))

# --- 서브카테고리 API ---
@app.route("/api/sub_categories", methods=["GET"])
def get_sub_categories():
    return jsonify(sub_categories_df.to_dict(orient="records"))

# --- 브랜드 API ---
@app.route("/api/brands", methods=["GET"])
def get_brands():
    return jsonify(brands_df.to_dict(orient="records"))

# --- 렌탈사 API ---
@app.route("/api/rental_companies", methods=["GET"])
def get_rental_companies():
    return jsonify(rental_companies_df.to_dict(orient="records"))

# --- 제품 리스트 API ---
@app.route("/api/products", methods=["GET"])
def get_products():
    main_category_id = request.args.get("main_category_id", type=int)
    sub_category_id = request.args.get("sub_category_id", type=int)
    brand_id = request.args.get("brand_id", type=int)
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 15, type=int)

    df = products_df.copy()

    if main_category_id:
        df = df[df["main_category_id"] == main_category_id]
    if sub_category_id:
        df = df[df["sub_category_id"] == sub_category_id]
    if brand_id:
        df = df[df["brand_id"] == brand_id]

    total = len(df)
    start = (page - 1) * limit
    end = start + limit
    data = df.iloc[start:end].to_dict(orient="records")

    return jsonify({
        "total": total,
        "page": page,
        "limit": limit,
        "data": data,
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)