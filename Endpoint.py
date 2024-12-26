# en este codigo se creara un servidor endpoint con el objetivo de ingresar una Url
# y sean extraidos todos los contenidos <p> de una pagina, en la cual se eligio
# de tipo conocimiento y noticias multilenguaje,Funciona mucho mejor en web
# Wikipedia, Enciclopedia, La tercera, que posean <p>


from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

app = Flask(__name__)

# Inicializa el modelo de la Ia desde hugging face
tokenizer = AutoTokenizer.from_pretrained("tabularisai/multilingual-sentiment-analysis")
model = AutoModelForSequenceClassification.from_pretrained("tabularisai/multilingual-sentiment-analysis")

# Función para extraer párrafos de una URL
def scrape_paragraphs(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
    return paragraphs

# Función para analizar el sentimiento de un texto
def analyze_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=1)
    sentiment_scores = probabilities.tolist()[0]
    labels = ["negative", "neutral", "positive"]
    return {labels[i]: sentiment_scores[i] for i in range(len(labels))}

# Endpoint para realizar el scraping
@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({"error": "URL is required."}), 400
        paragraphs = scrape_paragraphs(url)
        output_file = 'paragraphs.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(paragraphs, f, ensure_ascii=False, indent=4)
        return jsonify({"message": "Paragraphs scraped and saved successfully.", "output_file": output_file}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para analizar el sentimiento de un texto
@app.route('/process', methods=['POST'])
def process_text():
    try:
        data = request.get_json()
        if 'text' not in data:
            return jsonify({"error": "El campo 'text' es requerido."}), 400
        text = data['text']
        sentiment = analyze_sentiment(text)
        return jsonify({"sentiment": sentiment})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/combined', methods=['POST'])
def combined():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({"error": "URL is required."}), 400

        # Scraping de la URL
        paragraphs = scrape_paragraphs(url)

        # Analizar el sentimiento de todos los párrafos concatenados
        full_text = " ".join(paragraphs)
        sentiment = analyze_sentiment(full_text)

        # Guardar los párrafos extraídos
        output_file = 'combined_paragraphs.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(paragraphs, f, ensure_ascii=False, indent=4)

        return jsonify({
            "message": "Paragraphs scraped and sentiment analyzed successfully.",
            "output_file": output_file,
            "sentiment": sentiment
        }), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
