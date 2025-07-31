from flask import Flask, request, jsonify
import csv
import ast

app = Flask(__name__)

# CSV 파일 경로
PRODUCTS_CSV = 'products.csv'
PRICES_CSV = 'prices.csv'
RENTAL_COMPANIES_CSV = 'rental_companies.csv'

def load_csv(path):
    """CSV 파일을 리스트[dict]로 변환"""
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

@app.route('/api/products')
def get_products():
    products = load_csv(PRODUCTS_CSV)
    # 옵션 컬럼이 문자열(dict형태)이면 진짜 dict로 파싱
    for prod in products:
        if 'options' in prod and isinstance(prod['options'], str):
            try:
                prod['options'] = ast.literal_eval(prod['options'])
            except Exception:
                prod['options'] = {}
    # 페이지네이션
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 30))
    start = (page - 1) * limit
    end = start + limit
    paginated = products[start:end]
    return jsonify({
        "total": len(products),
        "products": paginated
    })

@app.route('/api/prices')
def get_prices():
    prices = load_csv(PRICES_CSV)
    product_id = request.args.get('product_id')
    if product_id:
        prices = [row for row in prices if row.get('product_id') == str(product_id)]
    # 페이지네이션
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 30))
    start = (page - 1) * limit
    end = start + limit
    paginated = prices[start:end]
    return jsonify({
        "total": len(prices),
        "prices": paginated
    })

@app.route('/api/rental_companies')
def get_rental_companies():
    companies = load_csv(RENTAL_COMPANIES_CSV)
    return jsonify(companies)

# CORS 허용 (프론트와 연결시 필요하면)
from flask_cors import CORS
CORS(app)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)