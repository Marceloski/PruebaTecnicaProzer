# Esta request lo que hace es recibir por parametro una URL y hacerle scrapping
# luego de hacerle scrapping a la pagina dada, buscando todos los selectores <p>
# devuelve al usuario los parrafos de la pagina, y el sentimiento en formato json
# luego almacena ambos resultados en un archivo sqlite
# ejemplo : https://es.wikipedia.org/wiki/Lat%C3%ADn_medieval
import requests
import json
import sqlite3

def initialize_database():
    # Crea la base de datos y la tabla si no existen
    conn = sqlite3.connect("combined_logs.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            paragraphs TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()

def save_to_database(url, sentiment, paragraphs):
    # Guarda los datos en la base de datos
    conn = sqlite3.connect("combined_logs.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO logs (url, sentiment, paragraphs) 
        VALUES (?, ?, ?)
        """,
        (url, json.dumps(sentiment, ensure_ascii=False), json.dumps(paragraphs, ensure_ascii=False))
    )
    conn.commit()
    conn.close()

def make_combined_request():
    # URL del endpoint
    url = "http://127.0.0.1:5000/combined"
    texto_usuario = input("Ingrese una URL a Analizar Sentimiento")
    # Datos para la solicitud
    payload = {
        "url": texto_usuario
    }

    try:
        # Realizar la solicitud POST
        response = requests.post(url, json=payload)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            print("Respuesta del servidor:")
            response_data = response.json()
            print(json.dumps(response_data, indent=4, ensure_ascii=False))

            # Guardar el resultado en un archivo JSON
            output_file = "combined_response.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(response_data, f, ensure_ascii=False, indent=4)
            print(f"Archivo guardado como '{output_file}'")

            # Guardar en la base de datos
            save_to_database(
                payload["url"], 
                response_data.get("sentiment", {}), 
                response_data.get("output_file", "")
            )
            print("Datos guardados en la base de datos.")

        else:
            print(f"Error: Código de estado {response.status_code}")
            print(response.json())

    except Exception as e:
        print(f"Error al realizar la solicitud: {e}")

if __name__ == "__main__":
    initialize_database()
    make_combined_request()
