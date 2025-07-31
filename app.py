import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def read_csv(filename):
    return pd.read_csv(os.path.join(BASE_DIR, filename))

products = read_csv("products.csv")
main_categories = read_csv("main_categories.csv")
sub_categories = read_csv("sub_categories.csv")
brands = read_csv("brands.csv")

app = Flask(__name__)
CORS(app)

@app.route("/api/products")
def get_products():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 15))
    featured = request.args.get("featured", "false") == "true"
    main_category_id = request.args.get("main_category_id")
    sub_category_id = request.args.get("sub_category_id")
    brand_id = request.args.get("brand_id")
    q = request.args.get("q", "")

    df = products.copy()

    # 필터링
    if main_category_id:
        df = df[df["main_category_id"] == int(main_category_id)]
    if sub_category_id:
        df = df[df["sub_category_id"] == int(sub_category_id)]
    if brand_id:
        df = df[df["brand_id"] == int(brand_id)]
    if q:
        df = df[df["name"].str.contains(q, case=False, na=False)]

    # 페이지네이션
    start = (page-1) * limit
    end = start + limit
    result = df.iloc[start:end].to_dict(orient="records")
    return jsonify(result)

@app.route("/api/main_categories")
def get_main_categories():
    return jsonify(main_categories.to_dict(orient="records"))

@app.route("/api/sub_categories")
def get_sub_categories():
    return jsonify(sub_categories.to_dict(orient="records"))

@app.route("/api/brands")
def get_brands():
    return jsonify(brands.to_dict(orient="records"))

@app.route("/api")
def home():
    return jsonify({"msg": "Rental API Ready"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)