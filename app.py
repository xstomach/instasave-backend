from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')

    if not url or "instagram.com" not in url:
        return jsonify({"error": "Geçersiz bağlantı"}), 400

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        tag = soup.find('meta', property='og:video') or soup.find('meta', property='og:image')
        if tag and tag.get('content'):
            return jsonify({"media_url": tag['content']})
        else:
            return jsonify({"error": "Medya bulunamadı"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
