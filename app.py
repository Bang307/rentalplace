from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# 1. 데이터 로드 (앱 시작 시 한 번만)
products = pd.read_csv("products.csv", encoding="utf-8-sig")
prices = pd.read_csv("prices.csv", encoding="utf-8-sig")
rental_companies = pd.read_csv("rental_companies.csv", encoding="utf-8-sig")
main_categories = pd.read_csv("main_categories.csv", encoding="utf-8-sig")
sub_categories = pd.read_csv("sub_categories.csv", encoding="utf-8-sig")
brands = pd.read_csv("brands.csv", encoding="utf-8-sig")

# 2. 메인 카테고리 전체
@app.route("/api/main_categories")
def get_main_categories():
    result = main_categories.to_dict(orient="records")
    return jsonify(result)

# 3. 서브 카테고리 전체 (main_category_id로 필터링도 가능)
@app.route("/api/sub_categories")
def get_sub_categories():
    main_category_id = request.args.get("main_category_id")
    df = sub_categories
    if main_category_id:
        df = df[df["main_category_id"] == int(main_category_id)]
    return jsonify(df.to_dict(orient="records"))

# 4. 브랜드 전체
@app.route("/api/brands")
def get_brands():
    result = brands.to_dict(orient="records")
    return jsonify(result)

# 5. 렌탈사 전체
@app.route("/api/rental_companies")
def get_rental_companies():
    result = rental_companies.to_dict(orient="records")
    return jsonify(result)

# 6. 제품 목록 (페이징/필터/검색)
@app.route("/api/products")
def get_products():
    df = products.copy()

    # 필터링 (카테고리, 브랜드, 이름 검색 등)
    main_category_id = request.args.get("main_category_id")
    sub_category_id = request.args.get("sub_category_id")
    brand_id = request.args.get("brand_id")
    search = request.args.get("search")
    featured = request.args.get("featured")

    if main_category_id:
        df = df[df["main_category_id"] == int(main_category_id)]
    if sub_category_id:
        df = df[df["sub_category_id"] == int(sub_category_id)]
    if brand_id:
        df = df[df["brand_id"] == int(brand_id)]
    if search:
        mask = (
            df["name"].str.contains(search, case=False, na=False) |
            df["model"].astype(str).str.contains(search, case=False, na=False)
        )
        df = df[mask]
    if featured:
        # 예시: featured 컬럼 있으면 활용, 없으면 임시로 상위 10개
        if "featured" in df.columns:
            df = df[df["featured"] == 1]
        else:
            df = df.sort_values("id").head(10)

    # 페이징
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 30))
    start = (page - 1) * limit
    end = start + limit
    total = len(df)
    data = df.iloc[start:end].to_dict(orient="records")

    return jsonify({
        "total": total,
        "page": page,
        "limit": limit,
        "data": data
    })

# 7. 제품 상세 (id로 단건)
@app.route("/api/products/<int:product_id>")
def get_product_detail(product_id):
    df = products[products["id"] == product_id]
    if df.empty:
        return jsonify({"error": "Not found"}), 404
    return jsonify(df.iloc[0].to_dict())

# 8. 특정 제품 가격 리스트 (product_id로 필터링)
@app.route("/api/prices")
def get_prices():
    product_id = request.args.get("product_id")
    df = prices
    if product_id:
        df = df[df["product_id"] == int(product_id)]
    return jsonify(df.to_dict(orient="records"))

# 9. (선택) 건강 체크
@app.route("/api/ping")
def ping():
    return jsonify({"status": "ok"})

# --- 여기에 신청서 등 추가 가능 ---

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)