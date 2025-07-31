import pandas as pd
import ast
import json
from flask import Flask, jsonify, request
from flask_cors import CORS

# CSV 파일명
PRODUCTS_CSV = "products.csv"
MAIN_CATEGORIES_CSV = "main_categories.csv"
SUB_CATEGORIES_CSV = "sub_categories.csv"
BRANDS_CSV = "brands.csv"
PRICES_CSV = "prices.csv"
RENTAL_COMPANIES_CSV = "rental_companies.csv"

# 옵션 파싱 함수 (Python dict → JSON)
def parse_options(option_str):
    try:
        if isinstance(option_str, str):
            # 옵션이 NaN, 빈값이면 예외처리
            option_str = option_str.strip()
            if not option_str or option_str == "nan":
                return "{}"
            d = ast.literal_eval(option_str)
            return json.dumps(d, ensure_ascii=False)
        elif pd.isnull(option_str):
            return "{}"
        else:
            return json.dumps(option_str, ensure_ascii=False)
    except Exception:
        return "{}"

# 데이터프레임 캐싱
def load_products():
    df = pd.read_csv(PRODUCTS_CSV, encoding="utf-8")
    # 옵션 파싱 오류 방지
    if "options" in df.columns:
        df["options"] = df["options"].apply(parse_options)
    return df

def load_main_categories():
    return pd.read_csv(MAIN_CATEGORIES_CSV, encoding="utf-8")

def load_sub_categories():
    return pd.read_csv(SUB_CATEGORIES_CSV, encoding="utf-8")

def load_brands():
    return pd.read_csv(BRANDS_CSV, encoding="utf-8")

def load_prices():
    return pd.read_csv(PRICES_CSV, encoding="utf-8")

def load_rental_companies():
    return pd.read_csv(RENTAL_COMPANIES_CSV, encoding="utf-8")

# Flask 앱
app = Flask(__name__)
CORS(app)

# --- API 라우트 ---

@app.route("/api/main_categories")
def get_main_categories():
    df = load_main_categories()
    categories = df.to_dict(orient="records")
    return jsonify(categories)

@app.route("/api/sub_categories")
def get_sub_categories():
    df = load_sub_categories()
    categories = df.to_dict(orient="records")
    return jsonify(categories)

@app.route("/api/brands")
def get_brands():
    df = load_brands()
    brands = df.to_dict(orient="records")
    return jsonify(brands)

@app.route("/api/products")
def get_products():
    df = load_products()
    # 쿼리 파라미터
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 30))
    main_category_id = request.args.get("main_category_id", None)
    sub_category_id = request.args.get("sub_category_id", None)
    brand_id = request.args.get("brand_id", None)
    featured = request.args.get("featured", None)  # featured는 옵션이 없을 수 있음

    # 필터링
    if main_category_id:
        df = df[df["main_category_id"] == int(main_category_id)]
    if sub_category_id:
        df = df[df["sub_category_id"] == int(sub_category_id)]
    if brand_id:
        df = df[df["brand_id"] == int(brand_id)]
    # featured 추가하고 싶으면 여기에

    total = len(df)
    start = (page - 1) * limit
    end = start + limit
    items = df.iloc[start:end].to_dict(orient="records")
    return jsonify({
        "items": items,
        "total": total,
        "page": page,
        "limit": limit
    })

@app.route("/api/prices")
def get_prices():
    df = load_prices()
    prices = df.to_dict(orient="records")
    return jsonify(prices)

@app.route("/api/rental_companies")
def get_rental_companies():
    df = load_rental_companies()
    companies = df.to_dict(orient="records")
    return jsonify(companies)

# -- 헬스 체크(간단 연결 확인)
@app.route("/api/ping")
def ping():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)