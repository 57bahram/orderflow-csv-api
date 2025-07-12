
from flask import Flask, Response, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_csv():
    symbol = request.args.get('symbol', 'BTCUSDT')
    api_url = f"https://flask-orderflow-api.onrender.com/orderflow/{symbol}"

    try:
        res = requests.get(api_url, timeout=10)
        data = res.json()

        if 'mexc' not in data:
            return Response("price,type\n", mimetype='text/csv')

        lines = ["price,type"]
        for lvl in data["mexc"].get("supports", []):
            lines.append(f"{lvl['price']},support")
        for lvl in data["mexc"].get("resistances", []):
            lines.append(f"{lvl['price']},resistance")

        return Response("\n".join(lines), mimetype='text/csv')

    except Exception as e:
        return Response("price,type\n", mimetype='text/csv')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
