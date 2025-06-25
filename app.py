from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

data = [
    {"상품명": "나우 두께측정기 테스트용", "소비자금액": 10000000},
    {"상품명": "나우 결함탐상기 테스트용", "소비자금액": 50000000},
    {"상품명": "나우 약품 A", "소비자금액": 5000},
    {"상품명": "나우 약품 B", "소비자금액": 7000},
]
df = pd.DataFrame(data)

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

@app.route("/")
def home():
    return "Nawoo 가격 검색 API 작동 중"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
