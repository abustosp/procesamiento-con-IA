import os
import csv
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showinfo
from dotenv import load_dotenv
import os
import requests
import PyPDF2 as pypdf
import io
import json
from random import randint


def credenciales():
    
    load_dotenv(override=True)
    
    url = os.getenv("URL")    
    mail = os.getenv("MAIL")
    key = os.getenv("API_KEY")
    ia = os.getenv("IA")
    
    
    return url, mail, key, ia


def ia_data():
    
    load_dotenv(override=True)
    
    proveedor_ia = os.getenv("PROVEEDOR_IA")
    modelo_ia = os.getenv("MODELO_IA")
    url_ia = os.getenv("URL_IA")
    api_key_ia =os.getenv("API_KEY_IA")
    min_seed = os.getenv("MIN_SEED")
    max_seed = os.getenv("MAX_SEED")
    min_temperature = os.getenv("MIN_TEMPERATURE")
    max_temperature = os.getenv("MAX_TEMPERATURE")
    
    return proveedor_ia, modelo_ia, url_ia, api_key_ia, min_seed, max_seed, min_temperature, max_temperature


def agregar_datos_al_Response(prompt:str, 
                                seed:int, 
                                temperature:float, 
                                modelo:str, 
                                api_key:str, 
                                api_url:str, 
                                datos_originales:str,
                                proveedor_ia:str) -> str:
    
    prompt2 = prompt + datos_originales
    
    # Se envía el prompt, seed, temperature y modelo a la API
    if proveedor_ia.upper() == 'OLLAMA':    
        payload = {
            "model": modelo,
            "prompt": prompt2,
            "stream": False
        }
        options = {
            "seed": seed,
            "temperature": temperature
        }
        payload.update(options)
        
    else:
        payload = {
            "model": modelo,
            "messages": [{"role": "user", "content": prompt2}],
            "temperature": temperature,
            # "seed": seed,
            "n": 1,
            "max_tokens": 10000
        }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url=api_url, json=payload, headers=headers) 
        if proveedor_ia == 'OLLAMA':
            return response.json().get('response', datos_originales)
        else:
            return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"
        


def consulta_requests_restantes():
    
    url, mail, key, ia = credenciales()
    
    endpoint = f"{url}/users/remaining-queries/"
    
    params = {
        "email": mail,
        "api_key": key
    }
    
    response = requests.get(endpoint, params=params)
    
    return response.json()


def consulta_reconocedor_pdf_individual(pdf_path):
    
    url, mail, key, ia = credenciales()
    
    # Leer el archivo PDF completo
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = pypdf.PdfReader(pdf_file)
        first_page = pdf_reader.pages[0]

        # Crear un objeto PDF temporal solo con la primera página
        pdf_writer = pypdf.PdfWriter()
        pdf_writer.add_page(first_page)

        # Crear un archivo temporal en memoria para almacenar el PDF de la primera página
        temp_pdf_bytes = bytearray()
        with io.BytesIO() as temp_pdf_file:
            pdf_writer.write(temp_pdf_file)
            temp_pdf_file.seek(0)
            temp_pdf_bytes = temp_pdf_file.read()

    endpoint = f"{url}/analyze-invoice/"
    params = {
        "api_key": key,
        "email": mail
    }
    
    files = {
        "file": ("temp.pdf", temp_pdf_bytes, "application/pdf")
    }

    response = requests.post(endpoint, params=params, files=files)
    
    if ia.lower() == "si":
        # abrir el txt del prompt
        with open("promt-general.txt", "r") as prompt_file:
            prompt = prompt_file.read()
        proveedor_ia, modelo_ia, url_ia, api_key_ia, min_seed, max_seed, min_temperature, max_temperature = ia_data()
        response_json = response.json()
        if isinstance(response_json, list):
            for item in response_json:
                if "text" in item:
                    seed = randint(int(min_seed), int(max_seed))
                    temperature = randint(int(min_temperature*100), int(max_temperature*100))/100
                    item["Respuesta_IA"] = agregar_datos_al_Response(prompt, seed, temperature, modelo_ia, api_key_ia, url_ia, item["text"], proveedor_ia)
        elif "text" in response_json:
            seed = randint(int(min_seed), int(max_seed))
            temperature = randint(int(min_temperature*100), int(max_temperature*100))/100
            response_json["Respuesta_IA"] = agregar_datos_al_Response(prompt, seed, temperature, modelo_ia, api_key_ia, url_ia, response_json["text"], proveedor_ia)
        if isinstance(response_json, list):
            return {"original_response": response_json, "Respuesta_IA": [item.get("Respuesta_IA", "") for item in response_json]}
        else:
            return {"original_response": response_json, "Respuesta_IA": response_json.get("Respuesta_IA", "")}

    return {"original_response": response.json(), "Respuesta_IA": ""}


def select_folder_and_analyze_pdfs():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        os.listdir(folder_selected)
        result_folder = os.path.join(folder_selected, "Resultado")
        pdf_files = [file for file in os.listdir(folder_selected) if file.endswith(".pdf")]
        for pdf_file in pdf_files:
            pdf_path = os.path.join(folder_selected, pdf_file)
            response = consulta_reconocedor_pdf_individual(pdf_path)
            
            os.makedirs(result_folder, exist_ok=True)
            result_file = os.path.join(result_folder, f"{pdf_file}.json")
            
            json.dump(response, open(result_file, "w"))


if __name__ == "__main__":
    #url, mail, key = credenciales()
    response = consulta_requests_restantes()
    # response = consulta_reconocedor_pdf_individual(mail, url, "/home/abp/Downloads/20374730429_011_00001_00000120.pdf")
    # response = select_folder_and_analyze_pdfs()
    print(response)