from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/analizar-url', methods=['POST'])
def analizar_url():
    data = request.get_json()
    url = data['url']
    es_sospechosa = 'malicious.com' in url
    print("Analizando URL:", url)
    
    return jsonify({'sospechosa': es_sospechosa})

if __name__ == '__main__':
    app.run(debug=True)
