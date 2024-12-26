# PruebaTecnicaProzer
 
Esta es una Aplicacion creada para realizar un servidor local python de forma Endpoint
Se debe instalar al menos version de Node.js v20.10.0 y Python 3.12.1

ejecutando el comando para todas las dependencias

*npm install axios cheerio @huggingface/transformers torch*

Las request fueron realizadas exclusivamente en Lenguaje python
El uso requiere que se corra el archivo EndPoint.py

luego se pueden correr Request1, Request2, y Request3 de manera libre e independiente
en el ambito local


Adjunto esta el archivo Scrape, que contiene los metodos 
/Scrape: El cual recibe el script Request1, pidiendo una URL por pantalla
        dando como respuesta un archivo JSON con todos los selectores <p> 
        de una web.

/process: El cual recibe el scrip Request2, que pide un texto por teclado
        dando como respuesta un archivo de sentimiento sobre el texto 
        scrapeado de la URL proporcionada en especifico utilizando
        la IA de Huggingface https://huggingface.co/tabularisai/multilingual-sentiment-analysis
        y dejando un archivo JSON con el analisis del sentimiento

/combined: el cual recibe el script request3, que pide una url por teclado, realiza scrapping de la pagina
        devuelve el resultado del sentimiento de la IA de hugginface y dejando el archivo del sentimiento,
        creando si no hay una base de datos sqlite para guardar todos y cada uno de los archivos de sentimiento


