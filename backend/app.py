from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Inicializar la aplicación Flask
app = Flask(__name__)
CORS(app)

# Cargar el modelo y el tokenizador de Hugging Face
model_name = "bgspaditya/malurl-roberta-10e"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

labels = ["benign", "defacement", "malware", "phishing"]

@app.route('/analizar-url', methods=['POST'])
def analizar_url():
    # Obtención de la URL del cuerpo de la solicitud
    data = request.get_json()
    url = data['url']

    # Tokenización de la URL
    inputs = tokenizer(url, return_tensors="pt", truncation=True, max_length=512)

    # Realización de la inferencia con el modelo
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Obteneción de la predicción de la salida del modelo
    logits = outputs.logits
    predicted_class_id = torch.argmax(logits, dim=1).item()

    # Determinación de la etiqueta
    etiqueta = labels[predicted_class_id]

    es_sospechosa = etiqueta in ["phishing", "malware"]  # Etiquetas sospechosas

    # Imprimir y retornar el resultado
    print("Analizando URL:", url)
    print("Resultado del análisis:", "Sospechosa" if es_sospechosa else "Segura")

    return jsonify({'sospechosa': es_sospechosa, 'etiqueta': etiqueta})

if __name__ == '__main__':
    app.run(debug=True)
