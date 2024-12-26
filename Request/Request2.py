# Esta request lo que hace es recibir por parametro un texto y analizarlo
# devolviendo el sentimiento del texto y un archivo Json que 
# se actualiza con cada ejecucion
import requests
import json

def send_post_request():
    # URL del endpoint
    url = "http://127.0.0.1:5000/process"

    # Solicitar al usuario que ingrese el texto
    texto_usuario = input("Por favor, ingrese el texto a analizar: ")

    # Crear el payload con el texto proporcionado por el usuario
    payload = {
        "text": texto_usuario
    }

    try:
        # Envia la solicitud POST con el texto del usuario
        response = requests.post(url, json=payload)

        # Verifica si la respuesta es exitosa
        if response.status_code == 200:
            print("Respuesta del servidor:")
            print(response.json())

            # Guarda la respuesta en un archivo JSON
            with open("Respuesta_de_Sentimiento.json", "w", encoding="utf-8") as json_file:
                json.dump(response.json(), json_file, ensure_ascii=False, indent=4)
            print("Archivo guardado como 'Respuesta_de_Sentimiento.json'")
        else:
            print(f"Error: Código de estado {response.status_code}")
            print(response.json())

    except Exception as e:
        print(f"Error al realizar la solicitud: {e}")

if __name__ == "__main__":
    send_post_request()