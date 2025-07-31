import os
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_CSV = os.path.join(BASE_DIR, "products.csv")
PRICES_CSV = os.path.join(BASE_DIR, "prices.csv")
COMPANIES_CSV = os.path.join(BASE_DIR, "rental_companies.csv")
BRANDS_CSV = os.path.join(BASE_DIR, "brands.csv")
MAINCAT_CSV = os.path.join(BASE_DIR, "main_categories.csv")
SUBCAT_CSV = os.path.join(BASE_DIR, "sub_categories.csv")

def load_data():
    products = pd.read_csv(PRODUCTS_CSV, encoding="utf-8").fillna("")
    prices = pd.read_csv(PRICES_CSV, encoding="utf-8").fillna("")
    companies = pd.read_csv(COMPANIES_CSV, encoding="utf-8").fillna("")
    brands = pd.read_csv(BRANDS_CSV, encoding="utf-8").fillna("")
    maincats = pd.read_csv(MAINCAT_CSV, encoding="utf-8").fillna("")
    subcats = pd.read_csv(SUBCAT_CSV, encoding="utf-8").fillna("")
    return products, prices, companies, brands, maincats, subcats

PRODUCTS, PRICES, COMPANIES, BRANDS, MAINCATS, SUBCATS = load_data()
brand_id2name = dict(zip(BRANDS["id"], BRANDS["name"]))
maincat_id2name = dict(zip(MAINCATS["id"], MAINCATS["name"]))
subcat_id2name = dict(zip(SUBCATS["id"], SUBCATS["name"]))

app = Flask(__name__)
CORS(app)

@app.route("/api/products")
def api_products():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 30))
    search = request.args.get("search", "").lower()
    category_id = request.args.get("category_id", "")
    brand_id = request.args.get("brand_id", "")

    df = PRODUCTS.copy()
    if search:
        df = df[df["name"].str.lower().str.contains(search)]
    if category_id:
        df = df[df["main_category_id"] == int(category_id)]
    if brand_id:
        df = df[df["brand_id"] == int(brand_id)]

    total = len(df)
    df = df.iloc[(page-1)*limit:page*limit]

    results = []
    for _, row in df.iterrows():
        prod = row.to_dict()
        # options parsing
        try:
            prod["options"] = eval(prod.get("options", "{}")) if isinstance(prod.get("options"), str) else {}
        except:
            prod["options"] = {}
        # id→name도 추가 (id만 있는 곳에서 사용가능하게)
        prod["brand_name"] = brand_id2name.get(prod["brand_id"], "")
        prod["main_category_name"] = maincat_id2name.get(prod["main_category_id"], "")
        prod["sub_category_name"] = subcat_id2name.get(prod["sub_category_id"], "")
        results.append(prod)

    return jsonify({
        "total": total,
        "page": page,
        "limit": limit,
        "results": results,
        "brands": BRANDS.to_dict(orient="records"),
        "main_categories": MAINCATS.to_dict(orient="records"),
        "sub_categories": SUBCATS.to_dict(orient="records"),
    })

@app.route("/api/prices")
def api_prices():
    product_id = request.args.get("product_id")
    if not product_id:
        return jsonify([])
    df = PRICES[PRICES["product_id"] == int(product_id)]
    return jsonify(df.to_dict(orient="records"))

@app.route("/api/rental_companies")
def api_companies():
    return jsonify(COMPANIES.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))