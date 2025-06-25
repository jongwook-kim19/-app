from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load product price data (static for now)
df = pd.read_excel("2025년 영업부 가격 엑셀용 제작.xlsx", sheet_name=0)

@app.route("/search")
def search():
    query = request.args.get("q", "")
    result = df[df['상품명'].str.contains(query, case=False, na=False)]
    if not result.empty:
        name = result.iloc[0]['상품명']
        price = int(result.iloc[0]['소비자금액'])
        return jsonify({"상품명": name, "소비자금액": price})
    else:
        return jsonify({"result": "일치하는 상품이 없습니다."})

@app.route("/web")
def search_page():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>Nawoo 가격 검색</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f4f4f4; padding: 50px; }
            .container { background: white; padding: 20px; max-width: 500px; margin: auto; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            h2 { text-align: center; }
            input[type="text"] { width: 100%; padding: 10px; margin-top: 10px; border: 1px solid #ccc; border-radius: 4px; }
            button { width: 100%; padding: 10px; margin-top: 10px; background-color: #007BFF; color: white; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background-color: #0056b3; }
            .result { margin-top: 20px; font-size: 16px; color: #333; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>상품 가격 검색</h2>
            <input type="text" id="searchInput" placeholder="상품명을 입력하세요...">
            <button onclick="searchProduct()">검색</button>
            <div class="result" id="result"></div>
        </div>
        <script>
            async function searchProduct() {
                const query = document.getElementById('searchInput').value;
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML

