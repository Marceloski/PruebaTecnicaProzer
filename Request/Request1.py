# Esta request lo que hace es recibir por parametro una URL y hacerle scrapping
# utilizando el navegador por defecto del sistema donde esta alojado en endpoint
# En este caso utilizaremos wikis, enciclopedias y otros lugares de conocimiento
# Wikipedia, Encyclopedia, Britanica y otras wikis
# devolviendo como archivo json todos los selectores <p>
# solo funciona con URL directas de paginas visitadas
# ejemplo : https://es.wikipedia.org/wiki/Plantae
import requests

def scrape_request():
    # Solicitar la URL en teclado
    user_url = input("Introduce la URL para realizar el scraping: ")

    # Configurar la solicitud al servidor local
    url = "http://127.0.0.1:5000/scrape"
    payload = {"url": user_url}
    headers = {"Content-Type": "application/json"}

    # Realizar la solicitud POST
    response = requests.post(url, json=payload, headers=headers)

    # Procesar la respuesta y el tiempo de ejecucion
    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print("Error:", response.status_code, response.text)

if __name__ == "__main__":
    scrape_request()
