import pandas as pd
import os

BASE_DIR = r"C:\Users\bangm\OneDrive - bu.ac.kr\바탕 화면\rental-api"
products = pd.read_csv(os.path.join(BASE_DIR, "products.csv"), encoding="utf-8").fillna("")
prices = pd.read_csv(os.path.join(BASE_DIR, "prices.csv"), encoding="utf-8").fillna("")
companies = pd.read_csv(os.path.join(BASE_DIR, "rental_companies.csv"), encoding="utf-8").fillna("")

# brands 테이블 생성
brand_names = sorted(products["brand"].dropna().unique())
brands = pd.DataFrame({"id": range(1, len(brand_names)+1), "name": brand_names})
brands.to_csv(os.path.join(BASE_DIR, "brands.csv"), index=False, encoding="utf-8")

# main_categories 테이블 생성
maincat_names = sorted(products["main_category"].dropna().unique())
maincats = pd.DataFrame({"id": range(1, len(maincat_names)+1), "name": maincat_names})
maincats.to_csv(os.path.join(BASE_DIR, "main_categories.csv"), index=False, encoding="utf-8")

# sub_categories 테이블 생성
subcat_col = "sub_category" if "sub_category" in products.columns else "sub_cagory"
subcat_names = sorted(products[subcat_col].dropna().unique())
subcats = pd.DataFrame({"id": range(1, len(subcat_names)+1), "name": subcat_names})
subcats.to_csv(os.path.join(BASE_DIR, "sub_categories.csv"), index=False, encoding="utf-8")

# 각각의 id 매핑 생성
brand2id = {name: i+1 for i, name in enumerate(brand_names)}
maincat2id = {name: i+1 for i, name in enumerate(maincat_names)}
subcat2id = {name: i+1 for i, name in enumerate(subcat_names)}

# products에 id컬럼 추가
products["brand_id"] = products["brand"].map(brand2id).fillna(0).astype(int)
products["main_category_id"] = products["main_category"].map(maincat2id).fillna(0).astype(int)
products["sub_category_id"] = products[subcat_col].map(subcat2id).fillna(0).astype(int)

products.to_csv(os.path.join(BASE_DIR, "products.csv"), index=False, encoding="utf-8")