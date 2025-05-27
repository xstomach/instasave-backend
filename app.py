from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # CORS açıldı, frontend'den istek kabul eder

@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')

    if not url or "instagram.com" not in url:
        return jsonify({"error": "Geçersiz Instagram URL'si"}), 400

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return jsonify({"error": "Instagram sayfasına ulaşılamadı"}), 400

        soup = BeautifulSoup(res.text, 'html.parser')

        # Video ya da fotoğraf linki bul
        tag = soup.find('meta', property='og:video') or soup.find('meta', property='og:image')
        if tag and tag.get('content'):
            media_url = tag['content']
            return jsonify({"media_url": media_url})
        else:
            return jsonify({"error": "Medya bulunamadı"}), 404

    except Exception as e:
        return jsonify({"error": "Bir hata oluştu: " + str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
