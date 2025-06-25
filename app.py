
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

data = [
    {"상품명": "나우 두께측정기 테스트용", "소비자금액": 10000000},
    {"상품명": "나우 결함탐상기 테스트용", "소비자금액": 50000000},
    {"상품명": "나우 약품 A", "소비자금액": 5000},
    {"상품명": "나우 약품 B", "소비자금액": 7000},
]
df = pd.DataFrame(data)

@app.route("/")
def home():
    return "Nawoo 가격 검색 API 작동 중"

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").strip().lower()
    matched = df[df['상품명'].str.lower().str.contains(query)]
    if matched.empty:
        return jsonify({"result": "일치하는 상품이 없습니다."})
    result = matched.iloc[0]
    return jsonify({
        "상품명": result['상품명'],
        "소비자금액": result['소비자금액']
    })

@app.route("/web")
def search_page():
    return render_template_string('<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><title>Nawoo 가격 검색</title><style>body { font-family: Arial, sans-serif; background: #f4f4f4; padding: 50px; } .container { background: white; padding: 20px; max-width: 500px; margin: auto; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); } h2 { text-align: center; } input[type="text"] { width: 100%; padding: 10px; margin-top: 10px; border: 1px solid #ccc; border-radius: 4px; } button { width: 100%; padding: 10px; margin-top: 10px; background-color: #007BFF; color: white; border: none; border-radius: 4px; cursor: pointer; } button:hover { background-color: #0056b3; } .result { margin-top: 20px; font-size: 16px; color: #333; }</style></head><body><div class="container"><h2>상품 가격 검색</h2><input type="text" id="searchInput" placeholder="상품명을 입력하세요..."><button onclick="searchProduct()">검색</button><div class="result" id="result"></div></div><script>function searchProduct() { const query = document.getElementById('searchInput').value.trim(); const resultDiv = document.getElementById('result'); resultDiv.innerHTML = '검색 중...'; fetch(`/search?q=${encodeURIComponent(query)}`).then(res => res.json()).then(data => { if (data.result) { resultDiv.innerHTML = `<strong>${data.result}</strong>`; } else { resultDiv.innerHTML = `<strong>상품명:</strong> ${data['상품명']}<br><strong>소비자금액:</strong> ${data['소비자금액'].toLocaleString()} 원`; } }).catch(err => { resultDiv.innerHTML = '오류가 발생했습니다. 다시 시도해주세요.'; }); }</script></body></html>')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
